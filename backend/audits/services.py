from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import transaction

from pixelprowlers.notifications import safe_send_mail

from .dossier_services import attach_client_dossier
from .models import AuditDossier, AuditDossierCounter
from .questions import AUDIT_SERIES, QUESTION_IDS


def _score(value: float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def create_audit_number() -> str:
    year = datetime.now().year
    counter, _created = AuditDossierCounter.objects.select_for_update().get_or_create(year=year)
    counter.last_number += 1
    counter.save(update_fields=["last_number"])

    return f"AUD-{year}-{counter.last_number:06d}"


@transaction.atomic
def create_audit_dossier(**validated_data) -> AuditDossier:
    dossier = AuditDossier.objects.create(
        numero_dossier=create_audit_number(),
        **validated_data,
    )
    attach_client_dossier(dossier, phase=0, source="audit", metadata={"audit_numero": dossier.numero_dossier})
    return dossier


def calculate_audit_scores(reponses: dict[str, int]) -> dict:
    missing = [question_id for question_id in QUESTION_IDS if question_id not in reponses]
    unexpected = [question_id for question_id in reponses if question_id not in QUESTION_IDS]

    if missing or unexpected:
        raise ValueError("Les 20 réponses sont obligatoires.")

    scores_series = {}
    decimal_scores = {}

    for serie in AUDIT_SERIES:
        values = [int(reponses[question["id"]]) for question in serie["questions"]]

        if any(value < 0 or value > 10 for value in values):
            raise ValueError("Les réponses doivent être comprises entre 0 et 10.")

        serie_score = _score(sum(values) / len(values))
        decimal_scores[serie["id"]] = serie_score
        scores_series[serie["id"]] = {
            "label": serie["label"],
            "score": str(serie_score),
        }

    score_global = _score(sum(decimal_scores.values()) / len(decimal_scores))
    weakest_id = min(decimal_scores, key=decimal_scores.get)
    weakest_data = scores_series[weakest_id]

    return {
        "scores_series": scores_series,
        "score_global": score_global,
        "pilier_faible": weakest_data["label"],
        "pilier_faible_id": weakest_id,
    }


def _email_enabled() -> bool:
    return bool(getattr(settings, "DEFAULT_FROM_EMAIL", ""))


def notify_completed_audit(dossier: AuditDossier, score_global: Decimal) -> dict[str, str]:
    statuses = {
        "internal_email": "not_configured",
        "client_email": "not_configured",
    }
    internal_email = getattr(settings, "AUDIT_INTERNAL_EMAIL", "") or getattr(settings, "CONTACT_TO", "")

    if _email_enabled() and internal_email:
        statuses["internal_email"] = safe_send_mail(
            subject=f"[AUDIT] {dossier.numero_dossier} - score {score_global}/10",
            message="\n".join(
                [
                    f"Dossier : {dossier.numero_dossier}",
                    f"Client : {dossier.client_dossier.dossier_id if dossier.client_dossier_id else '-'}",
                    f"Score global : {score_global}/10",
                    f"Nom : {dossier.prenom} {dossier.nom}",
                    f"Type : {dossier.get_type_personne_display()}",
                    f"Structure : {dossier.nom_structure or '-'}",
                    f"Email : {dossier.email}",
                    f"Téléphone : {dossier.telephone}",
                ]
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            recipient_list=[internal_email],
        )

    if _email_enabled():
        statuses["client_email"] = safe_send_mail(
            subject=f"Audit PixelProwlers reçu - {dossier.numero_dossier}",
            message="\n".join(
                [
                    f"Bonjour {dossier.prenom},",
                    "",
                    "Votre dossier d'audit PixelProwlers a bien été reçu.",
                    f"Numéro de dossier : {dossier.numero_dossier}",
                    f"Dossier client : {dossier.client_dossier.dossier_id if dossier.client_dossier_id else '-'}",
                    "",
                    "Un consultant PixelProwlers reprendra votre dossier sous 48h avec une analyse détaillée et des recommandations personnalisées.",
                    "",
                    "PixelProwlers",
                ]
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            recipient_list=[dossier.email],
        )

    return statuses
