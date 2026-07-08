from __future__ import annotations

import re
import time

import graphene
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from audits.dossier_services import attach_client_dossier
from audits.models import ClientDossier
from pixelprowlers.notifications import safe_send_mail

from .models import Contact, ContactMessage, DiagnosticTicket, Formation, FormationRegistration, Lead, Service


SINGLE_LINE_FORBIDDEN = {"\r", "\n", "<", ">", "`"}
PHONE_PATTERN = re.compile(r"^[0-9+().\s-]{6,30}$")
CONTACT_MIN_FILL_SECONDS = 3
CONTACT_RATE_LIMIT_MAX = 5
CONTACT_RATE_LIMIT_WINDOW_SECONDS = 10 * 60


def _clean(value: str | None, max_length: int, field: str, *, required: bool = False) -> str:
    cleaned = (value or "").strip()
    if required and not cleaned:
        raise GraphQLError(f"{field} est obligatoire.")
    if len(cleaned) > max_length or any(char in cleaned for char in SINGLE_LINE_FORBIDDEN):
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


def _check_choice(value: str, valid_values: set[str], field: str) -> str:
    if value not in valid_values:
        raise GraphQLError(f"{field} est invalide.")
    return value


def _client_ip(info) -> str:
    request = getattr(getattr(info, "context", None), "request", getattr(info, "context", None))
    if request is None:
        return "unknown"
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_limit(info, action: str, limit: int, window: int) -> bool:
    key = f"crm:{action}:{_client_ip(info)}"
    count = cache.get(key, 0)
    if count >= limit:
        return False
    cache.set(key, count + 1, timeout=window)
    return True


class ContactMessageType(DjangoObjectType):
    class Meta:
        model = ContactMessage
        fields = "__all__"


class ContactType(DjangoObjectType):
    demand_label = graphene.String()
    email_confirmation = graphene.JSONString()
    messages = graphene.List(ContactMessageType)

    class Meta:
        model = Contact
        fields = "__all__"

    def resolve_demand_label(self, info):
        return self.get_demand_type_display() if self.demand_type else self.get_service_type_display()

    def resolve_email_confirmation(self, info):
        return {
            "status": self.notification_status.get("client_email", "not_configured"),
        }

    def resolve_messages(self, info):
        return self.messages.all()


class DiagnosticTicketType(DjangoObjectType):
    id = graphene.String()

    class Meta:
        model = DiagnosticTicket
        fields = "__all__"

    def resolve_id(self, info):
        return self.ticket_id


class LeadType(DjangoObjectType):
    class Meta:
        model = Lead
        fields = "__all__"


class FormationType(DjangoObjectType):
    class Meta:
        model = Formation
        fields = "__all__"


class FormationRegistrationType(DjangoObjectType):
    class Meta:
        model = FormationRegistration
        fields = "__all__"


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service
        fields = "__all__"


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


def _notify_contact_client(contact: Contact, origin: str | None = None) -> str:
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "CONTACT_FROM", "")
    if not from_email:
        return "not_configured"

    confirmation_url = f"{origin.rstrip('/')}/ticket/{contact.secret_token}" if origin else f"/ticket/{contact.secret_token}"
    return safe_send_mail(
        subject=f"Votre demande PixelProwlers - Ticket {contact.ticket_id}",
        message="\n".join(
            [
                f"Bonjour {contact.name},",
                "",
                "Votre demande a bien ete recue.",
                "",
                f"Suivi du ticket : {confirmation_url}",
                "",
                "PixelProwlers",
            ]
        ),
        from_email=from_email,
        recipient_list=[contact.email],
    )


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
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        company = graphene.String(required=False)
        phone = graphene.String(required=False)
        service_type = graphene.String(required=True)
        demand_type = graphene.String(required=False)
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

    contact = graphene.Field(ContactType)
    detail = graphene.String()

    def mutate(self, info, **kwargs):
        if not _rate_limit(info, "contact", CONTACT_RATE_LIMIT_MAX, CONTACT_RATE_LIMIT_WINDOW_SECONDS):
            raise GraphQLError("Trop de demandes rapprochées. Réessayez plus tard.")
        if kwargs.get("website_company"):
            return CreateContact(contact=None, detail="Merci. Votre demande a bien été reçue.")
        started_at = kwargs.get("started_at")
        if not started_at or time.time() - (int(started_at) / 1000) < CONTACT_MIN_FILL_SECONDS:
            return CreateContact(contact=None, detail="Merci. Votre demande a bien été reçue.")
        if kwargs.get("privacy_consent") is False:
            raise GraphQLError("Le consentement est requis.")

        message = (kwargs.get("message") or "").strip()
        if len(message) < 20 or len(message) > 4000:
            raise GraphQLError("message doit contenir entre 20 et 4000 caractères.")

        service_type = _check_choice(kwargs["service_type"], {choice.value for choice in Contact.ServiceType}, "serviceType")
        demand_type = kwargs.get("demand_type") or ""
        contact = Contact.objects.create(
            name=_clean(kwargs["name"], 160, "name", required=True),
            email=_clean_email(kwargs["email"]),
            company=_clean(kwargs.get("company"), 180, "company"),
            phone=_clean_phone(kwargs.get("phone")),
            service_type=service_type,
            demand_type=demand_type if demand_type in {choice.value for choice in Contact.DemandType} else "",
            message=message,
        )
        ContactMessage.objects.create(contact=contact, author=ContactMessage.Author.CUSTOMER, author_name=contact.name, message=message)
        attach_client_dossier(contact, phase=ClientDossier.Phase.CONTACT, source="contact", metadata={"contact_id": contact.id})
        contact.notification_status = _notify_contact(
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
        request = getattr(getattr(info, "context", None), "request", getattr(info, "context", None))
        origin = request.headers.get("origin") if request is not None and hasattr(request, "headers") else None
        contact.notification_status["client_email"] = _notify_contact_client(contact, origin=origin)
        contact.save(update_fields=["notification_status"])
        return CreateContact(contact=contact, detail="Merci. Votre demande a bien été reçue.")


class AddContactMessage(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        message = graphene.String(required=True)
        author_name = graphene.String(required=True)

    contact = graphene.Field(ContactType)

    def mutate(self, info, token, message, author_name):
        cleaned_message = (message or "").strip()
        if len(cleaned_message) < 2 or len(cleaned_message) > 2000:
            raise GraphQLError("message est invalide.")
        contact = Contact.objects.get(secret_token=_clean(token, 80, "token", required=True))
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


class CreateLead(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        company = graphene.String(required=False)
        phone = graphene.String(required=False)
        budget = graphene.String(required=False)
        project_description = graphene.String(required=True)
        timeline = graphene.String(required=False)
        lead_type = graphene.String(required=True)

    lead = graphene.Field(LeadType)

    def mutate(self, info, **kwargs):
        description = (kwargs.get("project_description") or "").strip()
        if len(description) < 10 or len(description) > 4000:
            raise GraphQLError("projectDescription est invalide.")
        lead = Lead.objects.create(
            name=_clean(kwargs["name"], 160, "name", required=True),
            email=_clean_email(kwargs["email"]),
            company=_clean(kwargs.get("company"), 180, "company"),
            phone=_clean_phone(kwargs.get("phone")),
            budget=_clean(kwargs.get("budget"), 80, "budget"),
            project_description=description,
            timeline=_clean(kwargs.get("timeline"), 120, "timeline"),
            lead_type=_check_choice(kwargs["lead_type"], {choice.value for choice in Lead.LeadType}, "leadType"),
        )
        attach_client_dossier(lead, phase=ClientDossier.Phase.CONTACT, source="lead", metadata={"lead_id": lead.id})
        return CreateLead(lead=lead)


class UpdateLeadStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.String(required=True)

    lead = graphene.Field(LeadType)

    def mutate(self, info, id, status):
        lead = Lead.objects.get(pk=id)
        lead.status = _check_choice(status, {choice.value for choice in Lead.Status}, "status")
        lead.save(update_fields=["status", "updated_at"])
        return UpdateLeadStatus(lead=lead)


class CreateFormation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        format_type = graphene.String(required=True)
        duration_hours = graphene.Int(required=True)
        price = graphene.Decimal(required=True)
        max_participants = graphene.Int(required=False)
        scheduled_dates = graphene.JSONString(required=False)
        active = graphene.Boolean(required=False)

    formation = graphene.Field(FormationType)

    def mutate(self, info, **kwargs):
        formation = Formation.objects.create(
            title=_clean(kwargs["title"], 180, "title", required=True),
            description=(kwargs["description"] or "").strip(),
            format_type=_check_choice(kwargs["format_type"], {choice.value for choice in Formation.FormatType}, "formatType"),
            duration_hours=max(1, int(kwargs["duration_hours"])),
            price=kwargs["price"],
            max_participants=max(1, int(kwargs.get("max_participants") or 10)),
            scheduled_dates=kwargs.get("scheduled_dates") or [],
            active=kwargs.get("active", True),
        )
        return CreateFormation(formation=formation)


class CreateFormationRegistration(graphene.Mutation):
    class Arguments:
        formation_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        company = graphene.String(required=False)
        phone = graphene.String(required=False)
        number_of_participants = graphene.Int(required=False)
        special_needs = graphene.String(required=False)

    registration = graphene.Field(FormationRegistrationType)

    def mutate(self, info, **kwargs):
        formation = Formation.objects.get(pk=kwargs["formation_id"], active=True)
        registration = FormationRegistration.objects.create(
            formation=formation,
            name=_clean(kwargs["name"], 160, "name", required=True),
            email=_clean_email(kwargs["email"]),
            company=_clean(kwargs.get("company"), 180, "company"),
            phone=_clean_phone(kwargs.get("phone")),
            number_of_participants=max(1, int(kwargs.get("number_of_participants") or 1)),
            special_needs=(kwargs.get("special_needs") or "").strip()[:1200],
        )
        attach_client_dossier(registration, phase=ClientDossier.Phase.CONTACT, source="formation", metadata={"registration_id": registration.id})
        return CreateFormationRegistration(registration=registration)


class UpdateFormationRegistrationStatus(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.String(required=True)

    registration = graphene.Field(FormationRegistrationType)

    def mutate(self, info, id, status):
        registration = FormationRegistration.objects.get(pk=id)
        registration.status = _check_choice(status, {choice.value for choice in FormationRegistration.Status}, "status")
        registration.save(update_fields=["status", "updated_at"])
        return UpdateFormationRegistrationStatus(registration=registration)


class UpsertService(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        service_category = graphene.String(required=True)
        icon = graphene.String(required=False)
        order = graphene.Int(required=False)

    service = graphene.Field(ServiceType)

    def mutate(self, info, **kwargs):
        service, _created = Service.objects.update_or_create(
            slug=_clean(kwargs["slug"], 80, "slug", required=True),
            defaults={
                "name": _clean(kwargs["name"], 160, "name", required=True),
                "description": (kwargs["description"] or "").strip(),
                "service_category": _check_choice(kwargs["service_category"], {choice.value for choice in Service.Category}, "serviceCategory"),
                "icon": _clean(kwargs.get("icon"), 80, "icon"),
                "order": int(kwargs.get("order") or 0),
            },
        )
        return UpsertService(service=service)


class DeleteCrmObject(graphene.Mutation):
    class Arguments:
        model = graphene.String(required=True)
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, model, id):
        models = {
            "contact": Contact,
            "lead": Lead,
            "formation": Formation,
            "registration": FormationRegistration,
            "service": Service,
        }
        model_class = models.get(model)
        if model_class is None:
            raise GraphQLError("model est invalide.")
        model_class.objects.filter(pk=id).delete()
        return DeleteCrmObject(ok=True)


class Query(graphene.ObjectType):
    contacts = graphene.List(ContactType, service_type=graphene.String(), read=graphene.Boolean())
    contact = graphene.Field(ContactType, id=graphene.ID(required=True))
    contact_by_token = graphene.Field(ContactType, token=graphene.String(required=True))
    unread_contacts = graphene.List(ContactType)
    diagnostic_ticket = graphene.Field(DiagnosticTicketType, ticket_id=graphene.String(required=True))

    leads = graphene.List(LeadType, lead_type=graphene.String(), status=graphene.String(), timeline=graphene.String())
    lead = graphene.Field(LeadType, id=graphene.ID(required=True))

    formations = graphene.List(FormationType, format_type=graphene.String(), active=graphene.Boolean())
    formation = graphene.Field(FormationType, id=graphene.ID(required=True))

    formation_registrations = graphene.List(FormationRegistrationType, formation_id=graphene.ID(), status=graphene.String())
    formation_registration = graphene.Field(FormationRegistrationType, id=graphene.ID(required=True))

    services = graphene.List(ServiceType, service_category=graphene.String())
    service = graphene.Field(ServiceType, id=graphene.ID(), slug=graphene.String())

    def resolve_contacts(root, info, service_type=None, read=None):
        qs = Contact.objects.all()
        if service_type:
            qs = qs.filter(service_type=service_type)
        if read is not None:
            qs = qs.filter(read=read)
        return qs

    def resolve_contact(root, info, id):
        return Contact.objects.get(pk=id)

    def resolve_contact_by_token(root, info, token):
        return Contact.objects.get(secret_token=token)

    def resolve_unread_contacts(root, info):
        return Contact.objects.filter(read=False)

    def resolve_diagnostic_ticket(root, info, ticket_id):
        return DiagnosticTicket.objects.get(ticket_id=ticket_id)

    def resolve_leads(root, info, lead_type=None, status=None, timeline=None):
        qs = Lead.objects.all()
        if lead_type:
            qs = qs.filter(lead_type=lead_type)
        if status:
            qs = qs.filter(status=status)
        if timeline:
            qs = qs.filter(timeline=timeline)
        return qs

    def resolve_lead(root, info, id):
        return Lead.objects.get(pk=id)

    def resolve_formations(root, info, format_type=None, active=True):
        qs = Formation.objects.all()
        if active is not None:
            qs = qs.filter(active=active)
        if format_type:
            qs = qs.filter(format_type=format_type)
        return qs

    def resolve_formation(root, info, id):
        return Formation.objects.get(pk=id)

    def resolve_formation_registrations(root, info, formation_id=None, status=None):
        qs = FormationRegistration.objects.select_related("formation")
        if formation_id:
            qs = qs.filter(formation_id=formation_id)
        if status:
            qs = qs.filter(status=status)
        return qs

    def resolve_formation_registration(root, info, id):
        return FormationRegistration.objects.get(pk=id)

    def resolve_services(root, info, service_category=None):
        qs = Service.objects.all()
        if service_category:
            qs = qs.filter(service_category=service_category)
        return qs

    def resolve_service(root, info, id=None, slug=None):
        if slug:
            return Service.objects.get(slug=slug)
        return Service.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    add_contact_message = AddContactMessage.Field()
    create_diagnostic_ticket = CreateDiagnosticTicket.Field()
    create_lead = CreateLead.Field()
    update_lead_status = UpdateLeadStatus.Field()
    create_formation = CreateFormation.Field()
    create_formation_registration = CreateFormationRegistration.Field()
    update_formation_registration_status = UpdateFormationRegistrationStatus.Field()
    upsert_service = UpsertService.Field()
    delete_crm_object = DeleteCrmObject.Field()
