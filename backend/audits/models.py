import json
import hmac
import hashlib

from django.conf import settings
from django.db import models
from django.utils import timezone


class ClientDossier(models.Model):
    class Phase(models.IntegerChoices):
        CONTACT = 0, "Contact"
        DIAGNOSTIC = 1, "Diagnostic"
        PROPOSITION = 2, "Proposition"
        CONTRAT = 3, "Contrat"
        EN_COURS = 4, "En cours"
        TESTS_RECETTE = 5, "Tests / recette"
        LIVRAISON = 6, "Livraison"
        SUIVI = 7, "Suivi"
        ARCHIVE = 8, "Archivé"

    dossier_id = models.CharField(max_length=16, unique=True, db_index=True)
    sequence_month = models.CharField(max_length=4, db_index=True)
    sequence_number = models.PositiveIntegerField()
    phase = models.PositiveSmallIntegerField(choices=Phase.choices, default=Phase.CONTACT)
    email = models.EmailField(max_length=180, blank=True, db_index=True)
    name = models.CharField(max_length=180, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    source = models.CharField(max_length=40, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["sequence_month", "sequence_number"],
                name="client_dossier_month_sequence_unique",
            ),
        ]

    def __str__(self) -> str:
        return self.dossier_id

    def refresh_dossier_id(self) -> None:
        self.dossier_id = f"{self.sequence_month}{self.sequence_number:03d}-{self.phase}"

    def increment_phase(self, new_phase: int | None = None, changed_by=None, reason: str = "") -> "ClientDossier":
        old_phase = self.phase
        target_phase = self.phase + 1 if new_phase is None else int(new_phase)
        max_phase = max(choice.value for choice in self.Phase)
        target_phase = max(self.Phase.CONTACT, min(target_phase, max_phase))

        if target_phase == old_phase:
            return self

        self.phase = target_phase
        self.refresh_dossier_id()
        self.save(update_fields=["phase", "dossier_id", "updated_at"])
        DossierLog.objects.create(
            dossier=self,
            old_phase=old_phase,
            new_phase=target_phase,
            changed_by=changed_by if getattr(changed_by, "is_authenticated", False) else None,
            reason=reason,
        )
        return self


class ClientDossierCounter(models.Model):
    sequence_month = models.CharField(max_length=4, unique=True)
    last_number = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-sequence_month"]

    def __str__(self) -> str:
        return f"{self.sequence_month}: {self.last_number}"


class DossierLog(models.Model):
    dossier = models.ForeignKey(ClientDossier, on_delete=models.CASCADE, related_name="logs")
    old_phase = models.PositiveSmallIntegerField(choices=ClientDossier.Phase.choices)
    new_phase = models.PositiveSmallIntegerField(choices=ClientDossier.Phase.choices)
    timestamp = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="client_dossier_logs",
    )
    reason = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["-timestamp"]


class AuditDossier(models.Model):
    class PersonType(models.TextChoices):
        INDIVIDU = "individu", "Individu"
        ASSOCIATION = "association", "Association"
        ENTREPRISE = "entreprise", "Entreprise"

    class Status(models.TextChoices):
        IDENTIFIE = "identifié", "Identifié"
        QUESTIONNAIRE_COMPLETE = "questionnaire_complété", "Questionnaire complété"

    numero_dossier = models.CharField(max_length=16, unique=True, db_index=True)
    prenom = models.CharField(max_length=80)
    nom = models.CharField(max_length=80)
    email = models.EmailField(max_length=180)
    telephone = models.CharField(max_length=24)
    type_personne = models.CharField(max_length=16, choices=PersonType.choices)
    nom_structure = models.CharField(max_length=180, blank=True, null=True)
    consentement_rgpd = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=32, choices=Status.choices, default=Status.IDENTIFIE)
    notification_status = models.JSONField(default=dict, blank=True)
    client_dossier = models.ForeignKey(
        ClientDossier, on_delete=models.SET_NULL, blank=True, null=True, related_name="audit_dossiers"
    )

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self) -> str:
        return self.numero_dossier


class AuditDossierCounter(models.Model):
    year = models.PositiveIntegerField(unique=True)
    last_number = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return f"{self.year}: {self.last_number}"


class AuditReponse(models.Model):
    dossier = models.OneToOneField(AuditDossier, on_delete=models.CASCADE, related_name="reponse")
    reponses = models.JSONField()
    scores_series = models.JSONField()
    score_global = models.DecimalField(max_digits=4, decimal_places=2)
    pilier_faible = models.CharField(max_length=80)
    date_soumission = models.DateTimeField(auto_now_add=True)

    # Traçabilité / preuve légale
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default="")
    nom_signataire = models.CharField(max_length=160, blank=True, default="")
    telephone_signataire = models.CharField(max_length=24, blank=True, default="")
    signature_hash = models.CharField(max_length=64, blank=True, default="")

    class Meta:
        ordering = ["-date_soumission"]

    def __str__(self) -> str:
        return f"{self.dossier.numero_dossier} - {self.score_global}/10"

    def compute_signature(self) -> str:
        sig_key = settings.AUDIT_SIGNATURE_KEY
        if not sig_key:
            raise RuntimeError("AUDIT_SIGNATURE_KEY n'est pas configuré")
        canonical = json.dumps(
            {
                "reponses": self.reponses,
                "score_global": str(self.score_global),
                "date_soumission": self.date_soumission.isoformat() if self.date_soumission else "",
                "ip_address": self.ip_address or "",
                "telephone_signataire": self.telephone_signataire or "",
                "nom_signataire": self.nom_signataire or "",
            },
            sort_keys=True,
        )
        return hmac.new(sig_key.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()

    def save(self, *args, **kwargs):
        if not self.pk and not self.signature_hash:
            super().save(*args, **kwargs)
            self.signature_hash = self.compute_signature()
            AuditReponse.objects.filter(pk=self.pk).update(signature_hash=self.signature_hash)
        else:
            super().save(*args, **kwargs)


class RefonteAudit(models.Model):
    class PersonType(models.TextChoices):
        INDIVIDU = "individu", "Individu"
        ASSOCIATION = "association", "Association"
        ENTREPRISE = "entreprise", "Entreprise"

    class AnalysisStatus(models.TextChoices):
        EN_COURS = "en_cours", "En cours d'analyse"
        TERMINE = "termine", "Terminé"
        ECHEC_PARTIEL = "echec_partiel", "Échec partiel"
        NON_ANALYSABLE = "non_analysable", "Non analysable"
        ECHEC = "echec", "Échec"

    reference = models.CharField(max_length=28, unique=True, db_index=True)
    prenom = models.CharField(max_length=80)
    nom = models.CharField(max_length=80)
    email = models.EmailField(max_length=180)
    telephone = models.CharField(max_length=24)
    type_personne = models.CharField(max_length=16, choices=PersonType.choices)
    nom_structure = models.CharField(max_length=180, blank=True, null=True)
    site_url = models.URLField(max_length=500)
    consentement_rgpd = models.BooleanField(default=False)
    reponses = models.JSONField()
    analysis_status = models.CharField(max_length=24, choices=AnalysisStatus.choices, default=AnalysisStatus.EN_COURS)
    technical_report = models.JSONField(default=dict, blank=True)
    pagespeed_report = models.JSONField(default=dict, blank=True)
    heuristic_report = models.JSONField(default=list, blank=True)
    analysis_error = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)
    client_dossier = models.ForeignKey(
        ClientDossier, on_delete=models.SET_NULL, blank=True, null=True, related_name="refonte_audits"
    )

    class Meta:
        ordering = ["-date_creation"]
        indexes = [
            models.Index(fields=["email"], name="refonte_email_idx"),
            models.Index(fields=["analysis_status"], name="refonte_status_idx"),
        ]

    def __str__(self) -> str:
        return self.reference


class Citation(models.Model):
    class Language(models.TextChoices):
        FR = "fr", "Français"
        EN = "en", "Anglais"
        LA = "la", "Latin"

    class Theme(models.TextChoices):
        ESPOIR = "espoir", "Espoir"
        RENOUVEAU = "renouveau", "Renouveau"
        RESILIENCE = "résilience", "Résilience"
        JOIE_DE_VIVRE = "joie de vivre", "Joie de vivre"
        AMOUR = "amour", "Amour"
        PAIX = "paix", "Paix"

    texte = models.TextField()
    numero = models.PositiveIntegerField(unique=True, db_index=True)
    auteur = models.CharField(max_length=140)
    source = models.CharField(max_length=180)
    langue = models.CharField(max_length=8, choices=Language.choices, default=Language.FR)
    theme = models.CharField(max_length=32, choices=Theme.choices, default=Theme.ESPOIR)
    actif = models.BooleanField(default=True)
    verifie = models.BooleanField(default=False)
    nb_affichages = models.PositiveIntegerField(default=0)
    annee = models.PositiveSmallIntegerField(blank=True, null=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["numero", "auteur", "source", "id"]
        indexes = [
            models.Index(fields=["auteur"], name="citation_auteur_idx"),
            models.Index(fields=["source"], name="citation_source_idx"),
            models.Index(fields=["langue"], name="citation_langue_idx"),
            models.Index(fields=["theme"], name="citation_theme_idx"),
            models.Index(fields=["actif", "verifie"], name="citation_publication_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.auteur} - {self.texte[:60]}"


class Motif(models.Model):
    class CreneauType(models.TextChoices):
        HORAIRE_PRECIS = "horaire_precis", "Horaire précis"
        DEMI_JOURNEE = "demi_journee", "Demi-journée"
        JOURNEE_COMPLETE = "journee_complete", "Journée complète"

    nom = models.CharField(max_length=120, unique=True)
    duree_minutes = models.PositiveIntegerField(default=60)
    creneau_type = models.CharField(max_length=24, choices=CreneauType.choices, default=CreneauType.HORAIRE_PRECIS)
    actif = models.BooleanField(default=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "nom"]

    def __str__(self) -> str:
        return self.nom


class RaisonAppel(models.Model):
    nom = models.CharField(max_length=160, unique=True)
    actif = models.BooleanField(default=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordre", "nom"]

    def __str__(self) -> str:
        return self.nom


class RdvContact(models.Model):
    prenom = models.CharField(max_length=80)
    nom = models.CharField(max_length=80)
    email = models.EmailField(max_length=180, db_index=True)
    telephone = models.CharField(max_length=40)
    audit_dossier = models.ForeignKey(
        AuditDossier, on_delete=models.SET_NULL, blank=True, null=True, related_name="rdv_contacts"
    )
    client_dossier = models.ForeignKey(
        ClientDossier, on_delete=models.SET_NULL, blank=True, null=True, related_name="rdv_contacts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nom", "prenom"]

    def __str__(self) -> str:
        return f"{self.prenom} {self.nom}"


class CreneauCalendrier(models.Model):
    class Statut(models.TextChoices):
        LIBRE = "libre", "Libre"
        RESERVE_AUDIT = "reserve_audit", "Réservé audit"
        RESERVE_INTERVENTION = "reserve_intervention", "Réservé intervention"
        BLOQUE = "bloque", "Bloqué"

    date = models.DateField(db_index=True)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    statut = models.CharField(max_length=24, choices=Statut.choices, default=Statut.LIBRE, db_index=True)
    motif_reserve = models.ForeignKey(
        Motif, on_delete=models.SET_NULL, blank=True, null=True, related_name="creneaux_reserves"
    )
    urgence = models.BooleanField(default=False)
    client = models.ForeignKey(RdvContact, on_delete=models.SET_NULL, blank=True, null=True, related_name="creneaux")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["date", "heure_debut"]
        indexes = [
            models.Index(fields=["date", "statut"], name="creneau_date_statut_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.date} {self.heure_debut}-{self.heure_fin} ({self.statut})"


class Rdv(models.Model):
    class Statut(models.TextChoices):
        CONFIRME = "confirme", "Confirmé"
        ANNULE = "annule", "Annulé"

    contact = models.ForeignKey(RdvContact, on_delete=models.PROTECT, related_name="rdvs")
    motif = models.ForeignKey(Motif, on_delete=models.PROTECT, related_name="rdvs")
    creneaux = models.ManyToManyField(CreneauCalendrier, related_name="rdvs")
    raisons = models.ManyToManyField(RaisonAppel, through="RdvRaison", related_name="rdvs", blank=True)
    urgence = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=16, choices=Statut.choices, default=Statut.CONFIRME)
    notification_status = models.JSONField(default=dict, blank=True)
    client_dossier = models.ForeignKey(
        ClientDossier, on_delete=models.SET_NULL, blank=True, null=True, related_name="rdvs"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"RDV {self.contact} - {self.motif}"


class RdvRaison(models.Model):
    rdv = models.ForeignKey(Rdv, on_delete=models.CASCADE)
    raison = models.ForeignKey(RaisonAppel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("rdv", "raison")


class RdvRappel(models.Model):
    class TypeRappel(models.TextChoices):
        VEILLE = "veille", "La veille"
        UNE_HEURE = "une_heure", "Une heure avant"

    rdv = models.ForeignKey(Rdv, on_delete=models.CASCADE, related_name="rappels")
    type_rappel = models.CharField(max_length=16, choices=TypeRappel.choices)
    scheduled_at = models.DateTimeField(db_index=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=16, default="pending")
    last_error = models.TextField(blank=True)

    class Meta:
        ordering = ["scheduled_at"]
        unique_together = ("rdv", "type_rappel")
