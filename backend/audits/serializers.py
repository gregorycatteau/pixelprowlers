import re
import unicodedata
from datetime import datetime
from secrets import token_hex
from urllib.parse import urlparse

from rest_framework import serializers

from .models import AuditDossier, AuditReponse, Citation, Motif, RaisonAppel, Rdv, RefonteAudit
from .rdv_services import reserve_rdv
from .refonte_analysis import schedule_refonte_analysis
from .refonte_questions import REFONTE_QUESTION_IDS
from .services import calculate_audit_scores, create_audit_dossier, notify_completed_audit


PHONE_FR_PATTERN = re.compile(r"^(?:\+33[1-9]\d{8}|0[1-9]\d{8})$")
EMAIL_SUSPICIOUS_PATTERN = re.compile(r"\s|@.*@")
INJECTION_PATTERN = re.compile(r"(<|>|--|/\*|\*/|;|\"|`|\$\{)")


def normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    without_controls = "".join(
        char for char in normalized
        if not unicodedata.category(char).startswith("C")
    )
    return re.sub(r"\s+", " ", without_controls).strip()


def has_injection_chars(value: str) -> bool:
    return bool(INJECTION_PATTERN.search(value))


def validate_human_name(value: str, label: str) -> str:
    cleaned = normalize_text(value)

    if len(cleaned) < 2 or len(cleaned) > 50:
        raise serializers.ValidationError(f"{label} doit contenir entre 2 et 50 caractères.")

    if has_injection_chars(cleaned):
        raise serializers.ValidationError(f"{label} contient des caractères refusés.")

    allowed_separators = {" ", "-", "'"}

    for char in cleaned:
        if char in allowed_separators:
            continue
        if not unicodedata.category(char).startswith("L"):
            raise serializers.ValidationError(f"{label} accepte uniquement des lettres, espaces, tirets et apostrophes.")

    return cleaned


def validate_structure_name(value: str) -> str:
    cleaned = normalize_text(value)

    if len(cleaned) < 2 or len(cleaned) > 100:
        raise serializers.ValidationError("Le nom de la structure doit contenir entre 2 et 100 caractères.")

    if has_injection_chars(cleaned):
        raise serializers.ValidationError("Le nom de la structure contient des caractères refusés.")

    allowed_separators = {" ", "-", "'", "&", "."}

    for char in cleaned:
        if char in allowed_separators:
            continue
        if not (unicodedata.category(char).startswith("L") or unicodedata.category(char).startswith("N")):
            raise serializers.ValidationError("Le nom de la structure contient un caractère non autorisé.")

    return cleaned


class AuditDossierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditDossier
        fields = [
            "numero_dossier",
            "prenom",
            "nom",
            "email",
            "telephone",
            "type_personne",
            "nom_structure",
            "consentement_rgpd",
        ]
        read_only_fields = ["numero_dossier"]

    def validate(self, attrs):
        attrs["prenom"] = validate_human_name(attrs.get("prenom", ""), "Le prénom")
        attrs["nom"] = validate_human_name(attrs.get("nom", ""), "Le nom")
        attrs["email"] = normalize_text(attrs.get("email", "")).lower()
        attrs["telephone"] = normalize_text(attrs.get("telephone", "")).replace(" ", "")

        if len(attrs["email"]) > 254 or EMAIL_SUSPICIOUS_PATTERN.search(attrs["email"]):
            raise serializers.ValidationError("L'email est invalide.")

        if has_injection_chars(attrs["email"]):
            raise serializers.ValidationError("L'email contient des caractères refusés.")

        if not PHONE_FR_PATTERN.match(attrs["telephone"]):
            raise serializers.ValidationError("Le téléphone doit être un numéro français valide.")

        type_personne = attrs.get("type_personne")
        nom_structure = normalize_text(attrs.get("nom_structure") or "")

        if type_personne in [AuditDossier.PersonType.ASSOCIATION, AuditDossier.PersonType.ENTREPRISE] and not nom_structure:
            raise serializers.ValidationError("Le nom de la structure est obligatoire.")

        if nom_structure:
            attrs["nom_structure"] = validate_structure_name(nom_structure)

        if type_personne == AuditDossier.PersonType.INDIVIDU:
            attrs["nom_structure"] = ""

        if not attrs.get("consentement_rgpd"):
            raise serializers.ValidationError("Le consentement RGPD est obligatoire.")

        return attrs

    def create(self, validated_data):
        return create_audit_dossier(**validated_data)


class AuditSubmitSerializer(serializers.Serializer):
    numero_dossier = serializers.CharField(max_length=16)
    reponses = serializers.DictField(child=serializers.IntegerField(min_value=0, max_value=10))

    def validate_numero_dossier(self, value):
        try:
            return AuditDossier.objects.get(numero_dossier=value)
        except AuditDossier.DoesNotExist as exc:
            raise serializers.ValidationError("Dossier introuvable.") from exc

    def validate(self, attrs):
        try:
            attrs["calculated"] = calculate_audit_scores(attrs["reponses"])
        except ValueError as exc:
            raise serializers.ValidationError(str(exc)) from exc

        return attrs

    def save(self, **kwargs):
        dossier = self.validated_data["numero_dossier"]
        calculated = self.validated_data["calculated"]
        reponse, _created = AuditReponse.objects.update_or_create(
            dossier=dossier,
            defaults={
                "reponses": self.validated_data["reponses"],
                "scores_series": calculated["scores_series"],
                "score_global": calculated["score_global"],
                "pilier_faible": calculated["pilier_faible"],
            },
        )
        dossier.statut = AuditDossier.Status.QUESTIONNAIRE_COMPLETE
        dossier.notification_status = notify_completed_audit(dossier, calculated["score_global"])
        dossier.save(update_fields=["statut", "notification_status"])

        return reponse


class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citation
        fields = ["id", "numero", "texte", "auteur", "source", "langue", "theme", "annee"]


def create_refonte_reference() -> str:
    today = datetime.now().strftime("%Y%m%d")
    for _attempt in range(10):
        reference = f"PXP-REFONTE-{today}-{token_hex(2).upper()}"
        if not RefonteAudit.objects.filter(reference=reference).exists():
            return reference
    raise serializers.ValidationError("Impossible de générer une référence unique.")


def validate_refonte_answer(value):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        cleaned = normalize_text(value)
        if len(cleaned) > 1200:
            raise serializers.ValidationError("Une réponse dépasse 1200 caractères.")
        if has_injection_chars(cleaned):
            raise serializers.ValidationError("Une réponse contient des caractères refusés.")
        return cleaned

    if isinstance(value, list):
        if len(value) > 12:
            raise serializers.ValidationError("Une réponse contient trop d'options.")
        return [validate_refonte_answer(item) for item in value]

    raise serializers.ValidationError("Format de réponse invalide.")


class RefonteAuditCreateSerializer(serializers.ModelSerializer):
    reponses = serializers.DictField()

    class Meta:
        model = RefonteAudit
        fields = [
            "reference",
            "prenom",
            "nom",
            "email",
            "telephone",
            "type_personne",
            "nom_structure",
            "site_url",
            "consentement_rgpd",
            "reponses",
            "analysis_status",
        ]
        read_only_fields = ["reference", "analysis_status"]

    def validate_site_url(self, value):
        cleaned = normalize_text(value)
        parsed = urlparse(cleaned)

        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise serializers.ValidationError("L'URL du site doit commencer par http:// ou https://.")

        if has_injection_chars(cleaned):
            raise serializers.ValidationError("L'URL contient des caractères refusés.")

        return cleaned

    def validate(self, attrs):
        attrs["prenom"] = validate_human_name(attrs.get("prenom", ""), "Le prénom")
        attrs["nom"] = validate_human_name(attrs.get("nom", ""), "Le nom")
        attrs["email"] = normalize_text(attrs.get("email", "")).lower()
        attrs["telephone"] = normalize_text(attrs.get("telephone", "")).replace(" ", "")

        if len(attrs["email"]) > 254 or EMAIL_SUSPICIOUS_PATTERN.search(attrs["email"]):
            raise serializers.ValidationError("L'email est invalide.")

        if has_injection_chars(attrs["email"]):
            raise serializers.ValidationError("L'email contient des caractères refusés.")

        if not PHONE_FR_PATTERN.match(attrs["telephone"]):
            raise serializers.ValidationError("Le téléphone doit être un numéro français valide.")

        type_personne = attrs.get("type_personne")
        nom_structure = normalize_text(attrs.get("nom_structure") or "")

        if type_personne in [RefonteAudit.PersonType.ASSOCIATION, RefonteAudit.PersonType.ENTREPRISE] and not nom_structure:
            raise serializers.ValidationError("Le nom de la structure est obligatoire.")

        if nom_structure:
            attrs["nom_structure"] = validate_structure_name(nom_structure)

        if type_personne == RefonteAudit.PersonType.INDIVIDU:
            attrs["nom_structure"] = ""

        if not attrs.get("consentement_rgpd"):
            raise serializers.ValidationError("Le consentement RGPD est obligatoire.")

        reponses = attrs.get("reponses") or {}
        missing = [question_id for question_id in REFONTE_QUESTION_IDS if question_id not in reponses]
        unexpected = [question_id for question_id in reponses if question_id not in REFONTE_QUESTION_IDS]

        if missing or unexpected:
            raise serializers.ValidationError("Les 20 réponses du questionnaire refonte sont obligatoires.")

        attrs["reponses"] = {
            question_id: validate_refonte_answer(reponses[question_id])
            for question_id in REFONTE_QUESTION_IDS
        }

        return attrs

    def create(self, validated_data):
        audit = RefonteAudit.objects.create(
            reference=create_refonte_reference(),
            analysis_status=RefonteAudit.AnalysisStatus.EN_COURS,
            **validated_data,
        )
        schedule_refonte_analysis(audit.id)
        return audit


class RefonteAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefonteAudit
        fields = [
            "reference",
            "prenom",
            "nom",
            "email",
            "telephone",
            "type_personne",
            "nom_structure",
            "site_url",
            "reponses",
            "analysis_status",
            "technical_report",
            "pagespeed_report",
            "heuristic_report",
            "analysis_error",
            "date_creation",
            "date_maj",
        ]


class MotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motif
        fields = ["id", "nom", "duree_minutes", "creneau_type"]


class RaisonAppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaisonAppel
        fields = ["id", "nom"]


class RdvReservationSerializer(serializers.Serializer):
    motif_id = serializers.IntegerField()
    date = serializers.DateField()
    heure_debut = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    heure_fin = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    urgence = serializers.BooleanField(default=False)
    prenom = serializers.CharField(max_length=80)
    nom = serializers.CharField(max_length=80)
    email = serializers.EmailField(max_length=180)
    telephone = serializers.CharField(max_length=40)
    raison_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    message = serializers.CharField(max_length=1200, allow_blank=True, required=False)

    def validate_motif_id(self, value):
        if not Motif.objects.filter(id=value, actif=True).exists():
            raise serializers.ValidationError("Motif indisponible.")
        return value

    def validate_raison_ids(self, value):
        existing_count = RaisonAppel.objects.filter(id__in=value, actif=True).count()
        if existing_count != len(set(value)):
            raise serializers.ValidationError("Une raison d'appel est indisponible.")
        return value

    def create(self, validated_data):
        motif = Motif.objects.get(id=validated_data["motif_id"], actif=True)
        slot = {
            "date": validated_data["date"].isoformat(),
            "heure_debut": validated_data["heure_debut"].strftime("%H:%M"),
            "heure_fin": validated_data["heure_fin"].strftime("%H:%M"),
        }
        contact_data = {
            "prenom": validated_data["prenom"].strip(),
            "nom": validated_data["nom"].strip(),
            "email": validated_data["email"].strip().lower(),
            "telephone": validated_data["telephone"].strip(),
        }
        return reserve_rdv(
            motif=motif,
            slot=slot,
            contact_data=contact_data,
            raison_ids=validated_data["raison_ids"],
            urgence=validated_data["urgence"],
            message=validated_data.get("message", "").strip(),
        )


class RdvSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField()
    motif = MotifSerializer()
    creneaux = serializers.SerializerMethodField()
    raisons = RaisonAppelSerializer(many=True)

    class Meta:
        model = Rdv
        fields = ["id", "contact", "motif", "creneaux", "raisons", "urgence", "message", "notification_status"]

    def get_contact(self, obj):
        return {
            "prenom": obj.contact.prenom,
            "nom": obj.contact.nom,
            "email": obj.contact.email,
            "telephone": obj.contact.telephone,
        }

    def get_creneaux(self, obj):
        return [
            {
                "date": creneau.date.isoformat(),
                "heure_debut": creneau.heure_debut.strftime("%H:%M"),
                "heure_fin": creneau.heure_fin.strftime("%H:%M"),
            }
            for creneau in obj.creneaux.order_by("date", "heure_debut")
        ]
