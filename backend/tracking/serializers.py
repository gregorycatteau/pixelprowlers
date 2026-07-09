from uuid import UUID

from django.core.exceptions import ValidationError

from audits.dossier_services import create_client_dossier
from audits.models import ClientDossier

from .models import VisitorSession, PageView, QuestionInteraction, TrackingEvent
from .utils import parse_user_agent, get_client_ip, extract_utm


class BaseInputValidator:
    def __init__(self, data=None, context=None, **kwargs):
        self.initial_data = data or {}
        self.context = context or {}
        self.validated_data = {}
        self.errors = {}

    def is_valid(self):
        try:
            attrs = dict(self.initial_data)
            for field in list(attrs):
                validator = getattr(self, f"validate_{field}", None)
                if validator:
                    attrs[field] = validator(attrs[field])
            self.validated_data = self.validate(attrs)
            self.errors = {}
            return True
        except ValidationError as exc:
            self.validated_data = {}
            self.errors = {"non_field_errors": exc.messages}
            return False

    def validate(self, attrs):
        return attrs

    def save(self, **kwargs):
        return self.create({**self.validated_data, **kwargs})


class SessionInitSerializer(BaseInputValidator):
    """Creates or updates a VisitorSession from client payload + server-side data."""

    def validate_session_id(self, value):
        if not value:
            raise ValidationError("session_id is required")
        try:
            return value if isinstance(value, UUID) else UUID(str(value))
        except (TypeError, ValueError) as exc:
            raise ValidationError("session_id is invalid") from exc

    def validate(self, attrs):
        for field in ["referrer", "utm_source", "utm_medium", "utm_campaign", "language"]:
            value = attrs.get(field)
            if value is None:
                continue
            cleaned = str(value).strip()
            if len(cleaned) > 500:
                raise ValidationError(f"{field} is too long")
            if any(char in cleaned for char in ["\r", "\n", "<", ">", "`"]):
                raise ValidationError(f"{field} contains forbidden characters")
            attrs[field] = cleaned or None
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        ip_address = self.context.get("ip_address")
        raw_ua = self.context.get("user_agent", "")

        if request is not None and not ip_address:
            ip_address = get_client_ip(request)

        if request is not None and not raw_ua:
            raw_ua = request.META.get("HTTP_USER_AGENT", "")

        parsed_ua = parse_user_agent(raw_ua)

        utm = {
            "utm_source": validated_data.get("utm_source"),
            "utm_medium": validated_data.get("utm_medium"),
            "utm_campaign": validated_data.get("utm_campaign"),
            "referrer": validated_data.get("referrer"),
        }

        if request is not None and not any(utm.values()):
            if request.method == "GET":
                utm = {**utm, **extract_utm(request.GET)}
            else:
                utm = {**utm, **extract_utm(request.POST)}

        client_dossier = create_client_dossier(
            source="tracking",
            phase=ClientDossier.Phase.CONTACT,
            metadata={"session_id": str(validated_data["session_id"])},
        )

        return VisitorSession.objects.create(
            session_id=validated_data["session_id"],
            client_dossier=client_dossier,
            ip_address=ip_address,
            user_agent=raw_ua,
            device_type=parsed_ua["device_type"],
            browser=parsed_ua["browser"],
            os=parsed_ua["os"],
            referrer=validated_data.get("referrer") or utm.get("referrer"),
            utm_source=validated_data.get("utm_source") or utm.get("utm_source"),
            utm_medium=validated_data.get("utm_medium") or utm.get("utm_medium"),
            utm_campaign=validated_data.get("utm_campaign") or utm.get("utm_campaign"),
            language=validated_data.get("language"),
        )

    def update(self, instance, validated_data):
        # Update last_seen_at by touching the record
        instance.save()  # auto_now handles last_seen_at
        # Update UTM if provided
        if validated_data.get("utm_source"):
            instance.utm_source = validated_data["utm_source"]
        if validated_data.get("utm_medium"):
            instance.utm_medium = validated_data["utm_medium"]
        if validated_data.get("utm_campaign"):
            instance.utm_campaign = validated_data["utm_campaign"]
        instance.save()
        return instance


class PageViewSerializer(BaseInputValidator):
    """Validates page view payloads."""

    def validate_url(self, value):
        value = (value or "").strip()
        if len(value) > 1000 or any(char in value for char in ["\r", "\n", "<", ">", "`"]):
            raise ValidationError("url is invalid")
        return value

    def validate_title(self, value):
        if value is None:
            return value
        value = value.strip()
        if len(value) > 300 or any(char in value for char in ["\r", "\n", "<", ">", "`"]):
            raise ValidationError("title is invalid")
        return value


class QuestionInteractionSerializer(BaseInputValidator):
    """Validates question interaction payloads and applies upsert logic."""

    def validate_time_spent_seconds(self, value):
        if value is not None and value < 0:
            raise ValidationError("time_spent_seconds must be non-negative")
        return value or 0.0

    def validate_revisit_count(self, value):
        if value is not None and value < 0:
            raise ValidationError("revisit_count must be non-negative")
        return value or 0

    def validate_order_index(self, value):
        if value is not None and value < 0:
            raise ValidationError("order_index must be non-negative")
        return value or 0

    def validate_question_id(self, value):
        value = (value or "").strip()
        if not value or len(value) > 100 or any(char in value for char in ["\r", "\n", "<", ">", "`"]):
            raise ValidationError("question_id is invalid")
        return value

    def validate_serie(self, value):
        if value is None:
            return value
        value = value.strip()
        if len(value) > 50 or any(char in value for char in ["\r", "\n", "<", ">", "`"]):
            raise ValidationError("serie is invalid")
        return value

    def create(self, validated_data):
        session = self.context["session"]
        question_id = validated_data["question_id"]
        time_spent = validated_data.get("time_spent_seconds", 0.0)
        order_index = validated_data.get("order_index", 0)

        # Upsert: find existing record for this session + question_id
        # (first interaction record; order_index may differ on revisit)
        existing = (
            QuestionInteraction.objects
            .filter(session=session, question_id=question_id)
            .order_by("created_at")
            .first()
        )

        if existing:
            # Increment revisit counter, update latest time spent and order
            existing.revisit_count += 1
            existing.time_spent_seconds = time_spent
            existing.order_index = order_index
            existing.save()
            return existing

        # New interaction
        return QuestionInteraction.objects.create(
            session=session,
            question_id=question_id,
            serie=validated_data.get("serie"),
            time_spent_seconds=time_spent,
            revisit_count=0,
            order_index=order_index,
        )


class TrackingEventSerializer(BaseInputValidator):
    """Validates generic tracking event payloads."""

    def validate_event_type(self, value):
        valid_types = [choice[0] for choice in TrackingEvent.EVENT_TYPE_CHOICES]
        if value not in valid_types:
            raise ValidationError(
                f"Invalid event_type. Must be one of: {valid_types}"
            )
        return value

    def validate_metadata(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValidationError("metadata must be a JSON object (dict)")
        if len(json_safe := str(value)) > 4000:
            raise ValidationError("metadata is too large")
        return value

    def validate_page_url(self, value):
        value = (value or "").strip()
        if len(value) > 1000 or any(char in value for char in ["\r", "\n", "<", ">", "`"]):
            raise ValidationError("page_url is invalid")
        return value
