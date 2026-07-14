from __future__ import annotations

import hashlib
import hmac
import json
import logging
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMultiAlternatives
from django.db import DatabaseError, transaction
from django.utils import timezone

from audits.dossier_services import attach_client_dossier
from audits.models import ClientDossier

from .models import Contact, ContactDailyCounter, ContactMessage

logger = logging.getLogger(__name__)
PARIS = ZoneInfo("Europe/Paris")


class DailyContactLimitReached(Exception):
    pass


@dataclass(frozen=True)
class ContactData:
    nom: str
    prenom: str
    email: str
    telephone: str
    objet: str
    message: str
    methode_contact: str
    company: str
    service_type: str
    demand_type: str


def _canonical_text(value: str | None) -> str:
    return unicodedata.normalize("NFC", value or "")


def canonical_contact_payload(contact: Contact) -> bytes:
    created_utc = contact.date_creation.astimezone(ZoneInfo("UTC")).isoformat(timespec="microseconds").replace("+00:00", "Z")
    payload = {
        "date_creation": created_utc,
        "email": _canonical_text(contact.email),
        "message": _canonical_text(contact.message),
        "methode_contact": contact.methode_contact,
        "nom": _canonical_text(contact.nom),
        "numero_dossier": contact.numero_dossier,
        "objet": _canonical_text(contact.objet),
        "prenom": _canonical_text(contact.prenom),
        "telephone": _canonical_text(contact.phone),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_contact_hmac(contact: Contact) -> str:
    secret = getattr(settings, "CONTACT_HMAC_SECRET", "")
    if not secret:
        raise ImproperlyConfigured("CONTACT_HMAC_SECRET is required to create contact dossiers.")
    return hmac.new(secret.encode("utf-8"), canonical_contact_payload(contact), hashlib.sha256).hexdigest()


def verify_contact_hmac(contact: Contact) -> bool:
    expected = compute_contact_hmac(contact)
    return hmac.compare_digest(contact.signature_hmac, expected)


def _next_dossier_number(now: datetime) -> str:
    business_date = timezone.localtime(now, PARIS).date()
    ContactDailyCounter.objects.bulk_create(
        [ContactDailyCounter(date=business_date, value=0)],
        ignore_conflicts=True,
    )
    counter = ContactDailyCounter.objects.select_for_update().get(date=business_date)
    if counter.value >= 999:
        raise DailyContactLimitReached("Daily contact dossier limit reached.")
    counter.value += 1
    counter.save(update_fields=["value", "updated_at"])
    return f"{business_date:%d%m%Y}{counter.value:03d}"


@transaction.atomic
def create_contact_dossier(data: ContactData, *, now: datetime | None = None) -> Contact:
    creation_time = now or timezone.now()
    numero_dossier = _next_dossier_number(creation_time)
    contact = Contact(
        ticket_id=numero_dossier,
        numero_dossier=numero_dossier,
        nom=data.nom,
        prenom=data.prenom,
        name=f"{data.prenom} {data.nom}".strip(),
        email=data.email,
        company=data.company,
        phone=data.telephone,
        service_type=data.service_type,
        demand_type=data.demand_type,
        objet=data.objet,
        methode_contact=data.methode_contact,
        message=data.message,
        date_creation=creation_time,
        statut_notification=Contact.NotificationStatus.PENDING,
    )
    contact.signature_hmac = compute_contact_hmac(contact)
    contact.save(force_insert=True)
    ContactMessage.objects.create(
        contact=contact,
        author=ContactMessage.Author.CUSTOMER,
        author_name=contact.name,
        message=contact.message,
    )
    attach_client_dossier(
        contact,
        phase=ClientDossier.Phase.CONTACT,
        source="contact",
        metadata={"contact_id": contact.id, "numero_dossier": numero_dossier},
    )
    return contact


def send_contact_acknowledgement(contact: Contact) -> str:
    received_at = timezone.localtime(contact.date_creation, PARIS).strftime("%d/%m/%Y à %H:%M")
    subject = f"PixelProwlers — réception de votre demande n° {contact.numero_dossier}"
    text = "\n".join(
        [
            f"Bonjour {contact.prenom},",
            "",
            "Votre demande a bien été reçue.",
            f"Numéro de dossier : {contact.numero_dossier}",
            f"Date de réception : {received_at}",
            f"Objet : {contact.objet}",
            "",
            "Elle sera traitée dans les meilleurs délais.",
            "Cet email est un accusé de réception automatique.",
            "",
            "PixelProwlers",
        ]
    )
    html = (
        f"<p>Bonjour {escape(contact.prenom)},</p>"
        "<p>Votre demande a bien été reçue.</p>"
        f"<ul><li>Numéro de dossier : <strong>{contact.numero_dossier}</strong></li>"
        f"<li>Date de réception : {escape(received_at)}</li>"
        f"<li>Objet : {escape(contact.objet)}</li></ul>"
        "<p>Elle sera traitée dans les meilleurs délais.</p>"
        "<p><small>Cet email est un accusé de réception automatique.</small></p>"
        "<p>PixelProwlers</p>"
    )
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact.email],
        )
        email.attach_alternative(html, "text/html")
        email.send(fail_silently=False)
    except Exception as exc:
        logger.error(
            "contact_email_failed numero_dossier=%s error_type=%s",
            contact.numero_dossier,
            type(exc).__name__,
        )
        _update_notification(contact, Contact.NotificationStatus.FAILED)
        return Contact.NotificationStatus.FAILED

    _update_notification(contact, Contact.NotificationStatus.SENT, sent_at=timezone.now())
    return Contact.NotificationStatus.SENT


def _update_notification(contact: Contact, status: str, *, sent_at: datetime | None = None) -> None:
    try:
        Contact.objects.filter(pk=contact.pk).update(
            statut_notification=status,
            date_notification=sent_at,
            notification_status={"client_email": status},
        )
    except DatabaseError as exc:
        logger.error(
            "contact_notification_status_update_failed numero_dossier=%s error_type=%s",
            contact.numero_dossier,
            type(exc).__name__,
        )
        return
    contact.statut_notification = status
    contact.date_notification = sent_at
    contact.notification_status = {"client_email": status}
