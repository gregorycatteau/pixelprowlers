from graphene_django import DjangoObjectType

from .models import UrgencyRequest


class UrgencyRequestType(DjangoObjectType):
    class Meta:
        model = UrgencyRequest
        fields = [
            "id",
            "reference",
            "problem_type",
            "impact_level",
            "affected_url",
            "short_description",
            "since_when",
            "name",
            "organization",
            "email",
            "phone",
            "contact_preference",
            "callback_slot",
            "expected_next_step",
            "consent_to_contact",
            "no_secrets_confirmed",
            "status",
            "notification_status",
            "created_at",
        ]
