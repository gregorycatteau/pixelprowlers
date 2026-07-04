from datetime import datetime
from random import SystemRandom

from django.conf import settings
from django.core.mail import send_mail

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
        # Email interne prioritaire : contient le nécessaire de triage, jamais de credentials.
        send_mail(
            subject=f"[URGENT] {ticket.reference} - {ticket.get_problem_type_display()}",
            message="\n".join(
                [
                    f"Référence : {ticket.reference}",
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
            fail_silently=False,
        )
        statuses["internal_email"] = "sent"

    if _email_enabled():
        send_mail(
            subject=f"Demande urgence reçue - {ticket.reference}",
            message="\n".join(
                [
                    f"Bonjour {ticket.name},",
                    "",
                    "Votre demande d'urgence PixelProwlers a bien été reçue.",
                    f"Référence de dossier : {ticket.reference}",
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
            fail_silently=False,
        )
        statuses["client_email"] = "sent"

    return statuses
