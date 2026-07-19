from __future__ import annotations

import logging
import re
import time
import unicodedata

import graphene
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import DatabaseError, transaction
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from audits.dossier_services import attach_client_dossier
from audits.models import ClientDossier
from pixelprowlers.graphql_security import enforce_capability_rate_limit
from pixelprowlers.notifications import safe_send_mail

from .contact_services import (
    ContactData,
    DailyContactLimitReached,
    create_contact_dossier,
    normalize_french_mobile,
    send_contact_acknowledgement,
)
from .models import Contact, ContactMessage, DiagnosticTicket


SINGLE_LINE_FORBIDDEN = {"\x00", "\r", "\n", "<", ">", "`"}
PHONE_PATTERN = re.compile(r"^[0-9+().\s-]{6,30}$")
CONTACT_MIN_FILL_SECONDS = 3
CONTACT_RATE_LIMIT_MAX = 5
CONTACT_RATE_LIMIT_WINDOW_SECONDS = 10 * 60
logger = logging.getLogger(__name__)


def _clean(
    value: str | None,
    max_length: int,
    field: str,
    *,
    required: bool = False,
    min_length: int = 0,
) -> str:
    normalized = unicodedata.normalize("NFC", value or "")
    if any(char in normalized for char in SINGLE_LINE_FORBIDDEN):
        raise GraphQLError(f"{field} est invalide.")
    cleaned = normalized.strip()
    if required and not cleaned:
        raise GraphQLError(f"{field} est obligatoire.")
    if len(cleaned) < min_length or len(cleaned) > max_length:
        raise GraphQLError(f"{field} est invalide.")
    return cleaned


def _clean_email(value: str) -> str:
    email = _clean(value, 254, "email", required=True).lower()
    try:
        validate_email(email)
    except ValidationError as exc:
        raise GraphQLError("email est invalide.") from exc
    return email


def _clean_phone(value: str | None) -> str:
    phone = _clean(value, 40, "phone")
    if phone and not PHONE_PATTERN.fullmatch(phone):
        raise GraphQLError("phone est invalide.")
    return phone


def _clean_contact_phone(value: str | None) -> str:
    phone = _clean(value, 40, "telephone", required=True)
    try:
        return normalize_french_mobile(phone)
    except ValueError as exc:
        raise GraphQLError("Indique un numéro de téléphone français valide.") from exc


def _check_choice(value: str, valid_values: set[str], field: str) -> str:
    if value not in valid_values:
        raise GraphQLError(f"{field} est invalide.")
    return value


def _client_ip(info) -> str:
    request = getattr(getattr(info, "context", None), "request", getattr(info, "context", None))
    if request is None:
        return "unknown"
    remote_addr = request.META.get("REMOTE_ADDR", "unknown")
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded and remote_addr in getattr(settings, "TRUSTED_PROXY_IPS", set()):
        return forwarded.rsplit(",", 1)[-1].strip()
    return remote_addr


def _rate_limit(info, action: str, limit: int, window: int) -> bool:
    key = f"crm:{action}:{_client_ip(info)}"
    if cache.add(key, 1, timeout=window):
        return True
    try:
        return cache.incr(key) <= limit
    except ValueError:
        cache.set(key, 1, timeout=window)
        return True


class ContactMessageType(DjangoObjectType):
    class Meta:
        model = ContactMessage
        fields = ("author", "author_name", "message", "created_at")


class ContactType(DjangoObjectType):
    demand_label = graphene.String()
    messages = graphene.List(ContactMessageType)

    class Meta:
        model = Contact
        fields = (
            "id",
            "ticket_id",
            "secret_token",
            "numero_dossier",
            "nom",
            "prenom",
            "name",
            "email",
            "company",
            "phone",
            "service_type",
            "demand_type",
            "objet",
            "methode_contact",
            "status",
            "message",
            "created_at",
            "updated_at",
            "client_dossier",
        )

    def resolve_demand_label(self, info):
        return self.get_demand_type_display() if self.demand_type else self.get_service_type_display()

    def resolve_messages(self, info):
        return self.messages.all()


class DiagnosticTicketType(DjangoObjectType):
    id = graphene.String()

    class Meta:
        model = DiagnosticTicket
        fields = (
            "ticket_id",
            "organization",
            "email",
            "phone",
            "message",
            "answers",
            "diagnostic_result",
            "email_confirmation",
        )

    def resolve_id(self, info):
        return self.ticket_id


def _notify_contact(contact: Contact, detail_fields: dict) -> dict[str, str]:
    internal_to = getattr(settings, "CONTACT_TO", "")
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "CONTACT_FROM", "")
    status = {"internal_email": "not_configured"}

    if internal_to and from_email:
        status["internal_email"] = safe_send_mail(
            subject=f"[PixelProwlers] Nouvelle demande - {contact.service_type}",
            message="\n".join(
                [
                    "Nouvelle demande PixelProwlers",
                    "",
                    f"Dossier client : {contact.client_dossier.dossier_id if contact.client_dossier_id else '-'}",
                    f"Nom : {contact.name}",
                    f"Email : {contact.email}",
                    f"Téléphone : {contact.phone or 'Non précisé'}",
                    f"Structure : {contact.company or 'Non précisée'}",
                    f"Besoin principal : {contact.service_type}",
                    "",
                    "Détails :",
                    *[f"{key}: {value}" for key, value in detail_fields.items() if value not in {"", None}],
                    "",
                    "Message :",
                    contact.message,
                ]
            ),
            from_email=from_email,
            recipient_list=[internal_to],
        )

    return status


def _diagnostic_scores(answers: dict) -> dict:
    urgency = 0
    fragility = 0
    dependency = 0

    if answers.get("stress") in {"site-slow", "single-person", "backups"}:
        urgency += 2
    if answers.get("siteState") == "fragile":
        fragility += 2
    if answers.get("dependency") == "one":
        dependency += 3
    elif answers.get("dependency") == "unclear":
        dependency += 2

    total = urgency + fragility + dependency
    path = "MAINTENANCE"
    if total >= 7:
        path = "CRITICAL"
    elif fragility >= 2:
        path = "AUDIT"
    elif dependency >= 2:
        path = "TRANSMISSION"
    elif urgency >= 2 or answers.get("stress") == "some" or answers.get("siteState") == "doubt":
        path = "AUDIT"

    return {
        "path": path,
        "scores": {
            "urgency": urgency,
            "fragility": fragility,
            "dependency": dependency,
            "total": total,
        },
        "timestamp": timezone.now().isoformat(),
    }


def _notify_diagnostic_client(ticket: DiagnosticTicket, origin: str | None = None) -> dict[str, str]:
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "CONTACT_FROM", "")
    if not from_email:
        return {"status": "not_configured"}

    result_url = f"{origin.rstrip('/')}/diagnostic-result/{ticket.ticket_id}" if origin else f"/diagnostic-result/{ticket.ticket_id}"
    status = safe_send_mail(
        subject=f"Votre diagnostic PixelProwlers - Ticket {ticket.ticket_id}",
        message="\n".join(
            [
                f"Bonjour {ticket.organization},",
                "",
                "Merci d'avoir repondu a notre diagnostic.",
                "",
                f"Votre analyse personnalisee : {result_url}",
                "",
                "PixelProwlers",
            ]
        ),
        from_email=from_email,
        recipient_list=[ticket.email],
    )
    return {"status": status}


class CreateContact(graphene.Mutation):
    class Arguments:
        nom = graphene.String(required=True)
        prenom = graphene.String(required=True)
        email = graphene.String(required=True)
        company = graphene.String(required=True)
        telephone = graphene.String(required=True)
        objet = graphene.String(required=True)
        methode_contact = graphene.String(required=True)
        service_type = graphene.String(required=True)
        demand_type = graphene.String(required=True)
        message = graphene.String(required=True)
        structure_type = graphene.String(required=False)
        urgency = graphene.String(required=False)
        contact_preference = graphene.String(required=False)
        website_url = graphene.String(required=False)
        cms = graphene.String(required=False)
        hosting = graphene.String(required=False)
        backups = graphene.String(required=False)
        access = graphene.String(required=False)
        budget = graphene.String(required=False)
        found_us = graphene.String(required=False)
        privacy_consent = graphene.Boolean(required=False)
        website_company = graphene.String(required=False)
        started_at = graphene.Float(required=False)

    success = graphene.Boolean()
    numero_dossier = graphene.String()
    message = graphene.String()

    def mutate(self, info, **kwargs):
        if not _rate_limit(info, "contact", CONTACT_RATE_LIMIT_MAX, CONTACT_RATE_LIMIT_WINDOW_SECONDS):
            raise GraphQLError("Trop de demandes rapprochées. Réessayez plus tard.")
        if kwargs.get("website_company"):
            return CreateContact(success=True, message="Merci. Votre demande a bien été reçue.")
        started_at = kwargs.get("started_at")
        if not started_at or time.time() - (int(started_at) / 1000) < CONTACT_MIN_FILL_SECONDS:
            return CreateContact(success=True, message="Merci. Votre demande a bien été reçue.")
        if kwargs.get("privacy_consent") is False:
            raise GraphQLError("Le consentement est requis.")

        message = (kwargs.get("message") or "").strip()
        if len(message) < 20 or len(message) > 4000 or "\x00" in message:
            raise GraphQLError("message doit contenir entre 20 et 4000 caractères.")

        service_type = _check_choice(kwargs["service_type"], {choice.value for choice in Contact.ServiceType}, "serviceType")
        method = _check_choice(
            kwargs["methode_contact"],
            {choice.value for choice in Contact.ContactMethod},
            "methodeContact",
        )
        telephone = _clean_contact_phone(kwargs.get("telephone"))
        demand_type = _check_choice(
            kwargs["demand_type"],
            {choice.value for choice in Contact.DemandType},
            "demandType",
        )
        data = ContactData(
            nom=_clean(kwargs["nom"], 100, "nom", required=True, min_length=2),
            prenom=_clean(kwargs["prenom"], 100, "prenom", required=True, min_length=2),
            email=_clean_email(kwargs["email"]),
            telephone=telephone,
            objet=_clean(kwargs["objet"], 200, "objet", required=True, min_length=2),
            message=message,
            methode_contact=method,
            company=_clean(kwargs["company"], 180, "company", required=True, min_length=2),
            service_type=service_type,
            demand_type=demand_type,
        )
        delivery_result = {}
        try:
            with transaction.atomic():
                contact = create_contact_dossier(data)
                transaction.on_commit(
                    lambda: delivery_result.update(client_status=send_contact_acknowledgement(contact))
                )
        except DailyContactLimitReached as exc:
            raise GraphQLError("La capacité quotidienne de demandes est atteinte. Réessayez demain.") from exc

        client_status = delivery_result.get("client_status", Contact.NotificationStatus.PENDING)
        internal_status = _notify_contact(
            contact,
            {
                "structure_type": _clean(kwargs.get("structure_type"), 80, "structureType"),
                "urgency": _clean(kwargs.get("urgency"), 80, "urgency"),
                "contact_preference": _clean(kwargs.get("contact_preference"), 80, "contactPreference"),
                "website_url": _clean(kwargs.get("website_url"), 240, "websiteUrl"),
                "cms": _clean(kwargs.get("cms"), 80, "cms"),
                "hosting": _clean(kwargs.get("hosting"), 120, "hosting"),
                "backups": _clean(kwargs.get("backups"), 80, "backups"),
                "access": _clean(kwargs.get("access"), 80, "access"),
                "budget": _clean(kwargs.get("budget"), 80, "budget"),
                "found_us": _clean(kwargs.get("found_us"), 80, "foundUs"),
            },
        )
        contact.notification_status = {
            "client_email": client_status,
            **internal_status,
        }
        try:
            Contact.objects.filter(pk=contact.pk).update(
                statut_notification=client_status,
                notification_status=contact.notification_status,
            )
        except DatabaseError as exc:
            logger.error(
                "contact_notification_summary_update_failed numero_dossier=%s error_type=%s",
                contact.numero_dossier,
                type(exc).__name__,
            )
        if client_status == Contact.NotificationStatus.SENT:
            public_message = "Votre demande a bien été enregistrée. Un accusé de réception vous a été envoyé."
        else:
            public_message = "Votre demande a bien été enregistrée. Conservez votre numéro de dossier."
        return CreateContact(
            success=True,
            numero_dossier=contact.numero_dossier,
            message=public_message,
        )


class AddContactMessage(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        message = graphene.String(required=True)
        author_name = graphene.String(required=True)

    contact = graphene.Field(ContactType)

    def mutate(self, info, token, message, author_name):
        enforce_capability_rate_limit(info, "contact-message")
        cleaned_message = (message or "").strip()
        if len(cleaned_message) < 2 or len(cleaned_message) > 2000:
            raise GraphQLError("message est invalide.")
        try:
            contact = Contact.objects.get(secret_token=_clean(token, 80, "token", required=True))
        except Contact.DoesNotExist as exc:
            raise GraphQLError("Ressource indisponible.") from exc
        ContactMessage.objects.create(
            contact=contact,
            author=ContactMessage.Author.CUSTOMER,
            author_name=_clean(author_name, 160, "authorName", required=True),
            message=cleaned_message,
        )
        contact.status = Contact.Status.WAITING_CUSTOMER
        contact.save(update_fields=["status", "updated_at"])
        return AddContactMessage(contact=contact)


class CreateDiagnosticTicket(graphene.Mutation):
    class Arguments:
        organization = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)
        message = graphene.String(required=True)
        answers = graphene.JSONString(required=True)

    ticket = graphene.Field(DiagnosticTicketType)
    redirect_to = graphene.String()

    def mutate(self, info, **kwargs):
        message = (kwargs.get("message") or "").strip()
        if len(message) < 2 or len(message) > 1000:
            raise GraphQLError("message est invalide.")
        answers = kwargs.get("answers") or {}
        if not isinstance(answers, dict):
            raise GraphQLError("answers est invalide.")
        ticket = DiagnosticTicket.objects.create(
            organization=_clean(kwargs["organization"], 160, "organization", required=True),
            email=_clean_email(kwargs["email"]),
            phone=_clean_phone(kwargs.get("phone")),
            message=message,
            answers=answers,
            diagnostic_result=_diagnostic_scores(answers),
        )
        attach_client_dossier(ticket, phase=ClientDossier.Phase.DIAGNOSTIC, source="diagnostic", metadata={"ticket_id": ticket.ticket_id})
        request = getattr(getattr(info, "context", None), "request", getattr(info, "context", None))
        origin = request.headers.get("origin") if request is not None and hasattr(request, "headers") else None
        ticket.email_confirmation = _notify_diagnostic_client(ticket, origin=origin)
        ticket.save(update_fields=["email_confirmation"])
        return CreateDiagnosticTicket(ticket=ticket, redirect_to=f"/diagnostic-result/{ticket.ticket_id}")


class Query(graphene.ObjectType):
    contact_by_token = graphene.Field(ContactType, token=graphene.String(required=True))
    diagnostic_ticket = graphene.Field(DiagnosticTicketType, ticket_id=graphene.String(required=True))

    def resolve_contact_by_token(root, info, token):
        enforce_capability_rate_limit(info, "contact")
        try:
            return Contact.objects.get(secret_token=token)
        except Contact.DoesNotExist as exc:
            raise GraphQLError("Ressource indisponible.") from exc

    def resolve_diagnostic_ticket(root, info, ticket_id):
        enforce_capability_rate_limit(info, "diagnostic")
        try:
            return DiagnosticTicket.objects.get(ticket_id=ticket_id)
        except DiagnosticTicket.DoesNotExist as exc:
            raise GraphQLError("Ressource indisponible.") from exc


class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    add_contact_message = AddContactMessage.Field()
    create_diagnostic_ticket = CreateDiagnosticTicket.Field()
