import re

from rest_framework import serializers

from .models import UrgencyRequest
from .services import create_urgency_reference


SECRET_PATTERNS = [
    re.compile(r"\b(password|passwd|pwd|token|api[_-]?key|secret|private[_-]?key|ssh-rsa|bearer)\b\s*[:=]", re.I),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.I),
    re.compile(r"\bghp_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]

SINGLE_LINE_FIELDS = {
    "affected_url",
    "since_when",
    "name",
    "organization",
    "email",
    "phone",
    "callback_slot",
}


class UrgencyRequestSerializer(serializers.ModelSerializer):
    website = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = UrgencyRequest
        fields = [
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
            "website",
        ]
        read_only_fields = ["reference"]

    def validate(self, attrs):
        if attrs.get("website"):
            raise serializers.ValidationError("Demande refusée.")

        for field, value in attrs.items():
            if not isinstance(value, str):
                continue

            if field in SINGLE_LINE_FIELDS and ("\r" in value or "\n" in value):
                raise serializers.ValidationError("Un champ contient un saut de ligne non autorisé.")

            if any(pattern.search(value) for pattern in SECRET_PATTERNS):
                raise serializers.ValidationError(
                    "La demande semble contenir un secret. Retirez tout mot de passe, token, clé privée ou accès sensible."
                )

        if not attrs.get("consent_to_contact") or not attrs.get("no_secrets_confirmed"):
            raise serializers.ValidationError("Les confirmations obligatoires doivent être cochées.")

        return attrs

    # Génère la référence au moment de la création, après validation stricte.
    def create(self, validated_data):
        validated_data.pop("website", None)
        return UrgencyRequest.objects.create(
            reference=create_urgency_reference(),
            **validated_data,
        )
