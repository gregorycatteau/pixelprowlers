from rest_framework import serializers

from .models import VisitorSession, PageView, QuestionInteraction, TrackingEvent
from .utils import parse_user_agent, get_client_ip, extract_utm


class SessionInitSerializer(serializers.Serializer):
    """Creates or updates a VisitorSession from client payload + server-side data."""

    session_id = serializers.UUIDField(required=True)
    referrer = serializers.CharField(required=False, allow_null=True, allow_blank=True, default=None)
    utm_source = serializers.CharField(required=False, allow_null=True, allow_blank=True, default=None)
    utm_medium = serializers.CharField(required=False, allow_null=True, allow_blank=True, default=None)
    utm_campaign = serializers.CharField(required=False, allow_null=True, allow_blank=True, default=None)
    language = serializers.CharField(required=False, allow_null=True, allow_blank=True, default=None)

    def validate_session_id(self, value):
        if not value:
            raise serializers.ValidationError("session_id is required")
        return value

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

        return VisitorSession.objects.create(
            session_id=validated_data["session_id"],
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


class PageViewSerializer(serializers.ModelSerializer):
    """Validates page view payloads."""

    class Meta:
        model = PageView
        fields = ["session", "url", "title"]
        read_only_fields = ["session"]

    session = serializers.PrimaryKeyRelatedField(read_only=True)


class QuestionInteractionSerializer(serializers.ModelSerializer):
    """Validates question interaction payloads and applies upsert logic."""

    class Meta:
        model = QuestionInteraction
        fields = ["session", "question_id", "serie", "time_spent_seconds", "revisit_count", "order_index"]

    session = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_time_spent_seconds(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("time_spent_seconds must be non-negative")
        return value or 0.0

    def validate_revisit_count(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("revisit_count must be non-negative")
        return value or 0

    def validate_order_index(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("order_index must be non-negative")
        return value or 0

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


class TrackingEventSerializer(serializers.ModelSerializer):
    """Validates generic tracking event payloads."""

    class Meta:
        model = TrackingEvent
        fields = ["session", "event_type", "page_url", "metadata"]

    session = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_event_type(self, value):
        valid_types = [choice[0] for choice in TrackingEvent.EVENT_TYPE_CHOICES]
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid event_type. Must be one of: {valid_types}"
            )
        return value

    def validate_metadata(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError("metadata must be a JSON object (dict)")
        return value
