from __future__ import annotations

import graphene
from django.core.cache import cache
from graphql import GraphQLError

from .models import UrgencyRequest
from .serializers import UrgencyRequestSerializer
from .services import notify_urgency
from .types import UrgencyRequestType


URGENCY_RATE_LIMIT = 5
URGENCY_RATE_WINDOW_SECONDS = 15 * 60


def _serializer_errors_to_message(errors) -> str:
    parts = []
    for field, messages in errors.items():
        if isinstance(messages, (list, tuple)):
            joined = " ".join(str(message) for message in messages)
        else:
            joined = str(messages)
        parts.append(f"{field}: {joined}")
    return " | ".join(parts) if parts else "Erreur de validation."


def _request_from_info(info):
    context = getattr(info, "context", None)
    return getattr(context, "request", context)


def _client_ip(request) -> str:
    if request is None:
        return "unknown"

    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_limit_key(request) -> str:
    return f"urgency-rate:{_client_ip(request)}"


def _check_rate_limit(request) -> bool:
    key = _rate_limit_key(request)
    count = cache.get(key, 0)
    if count >= URGENCY_RATE_LIMIT:
        return False
    cache.set(key, count + 1, timeout=URGENCY_RATE_WINDOW_SECONDS)
    return True


class CreateUrgencyRequest(graphene.Mutation):
    class Arguments:
        problem_type = graphene.String(required=True)
        impact_level = graphene.String(required=True)
        affected_url = graphene.String(required=True)
        short_description = graphene.String(required=True)
        since_when = graphene.String(required=True)
        name = graphene.String(required=True)
        organization = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        contact_preference = graphene.String(required=True)
        callback_slot = graphene.String(required=True)
        expected_next_step = graphene.String(required=True)
        consent_to_contact = graphene.Boolean(required=True)
        no_secrets_confirmed = graphene.Boolean(required=True)
        website = graphene.String(required=False)

    reference = graphene.String()
    status = graphene.String()
    message = graphene.String()
    client_email_status = graphene.String()
    ticket = graphene.Field(UrgencyRequestType)

    def mutate(self, info, **kwargs):
        request = _request_from_info(info)
        if not _check_rate_limit(request):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        serializer = UrgencyRequestSerializer(data=kwargs)
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        ticket = serializer.save()
        ticket.notification_status = notify_urgency(ticket)
        ticket.save(update_fields=["notification_status"])

        return CreateUrgencyRequest(
            reference=ticket.reference,
            status=ticket.status,
            message="Demande urgente enregistrée.",
            client_email_status=ticket.notification_status.get("client_email", "not_configured"),
            ticket=ticket,
        )


class Mutation(graphene.ObjectType):
    create_urgency_request = CreateUrgencyRequest.Field()


class Query(graphene.ObjectType):
    pass
