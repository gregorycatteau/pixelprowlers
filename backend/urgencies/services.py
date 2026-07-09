from datetime import datetime
from random import SystemRandom

from django.conf import settings

from pixelprowlers.notifications import safe_send_mail, send_sms_notification, send_webhook_notification

from .models import UrgencyRequest


_random = SystemRandom()


def create_urgency_reference() -> str:
    date_part = datetime.now().strftime("%Y%m%d")

    for _ in range(12):
        suffix = f"{_random.randrange(0, 10000):04d}"
        reference = f"PXP-URG-{date_part}-{suffix}"

        if not UrgencyRequest.objects.filter(reference=reference).exists():
            return reference

    raise RuntimeError("Impossible de générer une référence urgence unique.")


def _email_enabled() -> bool:
    return bool(getattr(settings, "DEFAULT_FROM_EMAIL", ""))


def notify_urgency(ticket: UrgencyRequest) -> dict[str, str]:
    statuses = {
        "internal_email": "not_configured",
        "client_email": "not_configured",
        "internal_sms": "skipped",
        "webhook": "not_configured",
    }

    internal_email = getattr(settings, "URGENCY_INTERNAL_EMAIL", "") or getattr(settings, "CONTACT_TO", "")

    if _email_enabled() and internal_email:
        statuses["internal_email"] = safe_send_mail(
            subject=f"[URGENT] {ticket.reference} - {ticket.get_problem_type_display()}",
            message="\n".join(
                [
                    f"Référence : {ticket.reference}",
                    f"Dossier client : {ticket.client_dossier.dossier_id if ticket.client_dossier_id else '-'}",
                    f"Impact : {ticket.get_impact_level_display()}",
                    f"URL : {ticket.affected_url}",
                    f"Depuis : {ticket.since_when}",
                    "",
                    f"Nom : {ticket.name}",
                    f"Structure : {ticket.organization}",
                    f"Email : {ticket.email}",
                    f"Téléphone : {ticket.phone}",
                    f"Prochaine étape souhaitée : {ticket.get_expected_next_step_display()}",
                    "",
                    "Description :",
                    ticket.short_description,
                ]
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            recipient_list=[internal_email],
        )

    if _email_enabled():
        statuses["client_email"] = safe_send_mail(
            subject=f"Demande urgence reçue - {ticket.reference}",
            message="\n".join(
                [
                    f"Bonjour {ticket.name},",
                    "",
                    "Votre demande d'urgence PixelProwlers a bien été reçue.",
                    f"Référence de dossier : {ticket.reference}",
                    f"Dossier client : {ticket.client_dossier.dossier_id if ticket.client_dossier_id else '-'}",
                    f"Prochaine étape souhaitée : {ticket.get_expected_next_step_display()}",
                    "",
                    "Ne transmettez aucun mot de passe, token, clé privée, accès administrateur ou information sensible.",
                    "Les modalités d'intervention seront vues après un premier échange humain.",
                    "Conservez les preuves utiles de votre côté : captures d'écran, messages d'erreur, horaires.",
                    "",
                    "PixelProwlers",
                    "https://pixelprowlers.io",
                ]
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL"),
            recipient_list=[ticket.email],
        )

    if ticket.impact_level in {UrgencyRequest.ImpactLevel.BLOCKED, UrgencyRequest.ImpactLevel.SECURITY_DATA_RISK}:
        statuses["internal_sms"] = send_sms_notification(
            to=getattr(settings, "INTERNAL_SMS_TO", "") or ticket.phone,
            message=f"PixelProwlers urgence {ticket.reference} - {ticket.get_impact_level_display()} - {ticket.affected_url}",
        )

    statuses["webhook"] = send_webhook_notification(
        payload={
            "type": "urgency.created",
            "reference": ticket.reference,
            "client_dossier": ticket.client_dossier.dossier_id if ticket.client_dossier_id else None,
            "problem_type": ticket.problem_type,
            "impact_level": ticket.impact_level,
            "affected_url": ticket.affected_url,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
        },
    )

    return statuses
