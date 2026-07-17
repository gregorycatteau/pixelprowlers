from __future__ import annotations

import hashlib
import hmac
import json
import logging
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.db import DatabaseError, transaction
from django.utils import timezone

from audits.dossier_services import attach_client_dossier
from audits.models import ClientDossier

from .models import Contact, ContactDailyCounter, ContactMessage

logger = logging.getLogger(__name__)
PARIS = ZoneInfo("Europe/Paris")
CONTACT_PHONE_PRESENTATIONS = (
    re.compile(r"^0[67][0-9]{8}$"),
    re.compile(r"^0[67](?: [0-9]{2}){4}$"),
    re.compile(r"^\+33[67][0-9]{8}$"),
    re.compile(r"^\+33 [67](?: [0-9]{2}){4}$"),
)


class DailyContactLimitReached(Exception):
    pass


def normalize_french_mobile(value: str | None) -> str:
    raw = value or ""
    if not any(pattern.fullmatch(raw) for pattern in CONTACT_PHONE_PRESENTATIONS):
        raise ValueError("telephone must be a valid French mobile number")
    compact = raw.replace(" ", "")
    return f"0{compact[3:]}" if compact.startswith("+33") else compact


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
    required_text = {
        "nom": data.nom,
        "prenom": data.prenom,
        "email": data.email,
        "company": data.company,
        "objet": data.objet,
        "message": data.message,
        "methode_contact": data.methode_contact,
        "service_type": data.service_type,
        "demand_type": data.demand_type,
    }
    missing = [field for field, value in required_text.items() if not (value or "").strip()]
    if missing:
        raise ValueError(f"required contact fields are missing: {', '.join(missing)}")
    try:
        validate_email(data.email)
    except ValidationError as exc:
        raise ValueError("email is invalid") from exc
    if data.methode_contact not in {choice.value for choice in Contact.ContactMethod}:
        raise ValueError("methode_contact is invalid")
    if data.service_type not in {choice.value for choice in Contact.ServiceType}:
        raise ValueError("service_type is invalid")
    if data.demand_type not in {choice.value for choice in Contact.DemandType}:
        raise ValueError("demand_type is invalid")
    normalized_phone = normalize_french_mobile(data.telephone)
    normalized_company = unicodedata.normalize("NFC", data.company or "").strip()
    if (
        len(normalized_company) < 2
        or len(normalized_company) > 180
        or any(char in (data.company or "") for char in ("\x00", "\r", "\n"))
    ):
        raise ValueError("company is invalid")
    creation_time = now or timezone.now()
    numero_dossier = _next_dossier_number(creation_time)
    contact = Contact(
        ticket_id=numero_dossier,
        numero_dossier=numero_dossier,
        nom=data.nom,
        prenom=data.prenom,
        name=f"{data.prenom} {data.nom}".strip()[:160],
        email=data.email,
        company=normalized_company,
        phone=normalized_phone,
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
    current_status = (
        Contact.objects.filter(pk=contact.pk)
        .values_list("statut_notification", flat=True)
        .first()
    )
    if current_status == Contact.NotificationStatus.SENT:
        logger.info(
            "contact_email_already_sent numero_dossier=%s action=skipped",
            contact.numero_dossier,
        )
        contact.statut_notification = current_status
        return current_status

    subject = f"PixelProwlers — réception de votre demande n° {contact.numero_dossier}"
    text = "\n".join(
        [
            f"Bonjour {contact.prenom},",
            "",
            "Nous avons bien reçu votre message et ne manquerons pas de revenir vers vous rapidement.",
            "",
            f"Votre numéro de dossier est : {contact.numero_dossier}",
            "",
            "Cordialement,",
            "L’équipe PixelProwlers.",
        ]
    )
    html = (
        f"<p>Bonjour {escape(contact.prenom)},</p>"
        "<p>Nous avons bien reçu votre message et ne manquerons pas de revenir vers vous rapidement.</p>"
        f"<p>Votre numéro de dossier est : <strong>{contact.numero_dossier}</strong></p>"
        "<p>Cordialement,<br>L’équipe PixelProwlers.</p>"
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
