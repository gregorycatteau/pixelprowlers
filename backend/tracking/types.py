from graphene_django import DjangoObjectType

from .models import PageView, QuestionInteraction, TrackingEvent, VisitorSession


class VisitorSessionType(DjangoObjectType):
    class Meta:
        model = VisitorSession
        fields = [
            "id",
            "session_id",
            "ip_address",
            "user_agent",
            "device_type",
            "browser",
            "os",
            "referrer",
            "utm_source",
            "utm_medium",
            "utm_campaign",
            "language",
            "client_dossier",
            "created_at",
            "last_seen_at",
        ]


class PageViewType(DjangoObjectType):
    class Meta:
        model = PageView
        fields = ["id", "session", "url", "title", "created_at"]


class QuestionInteractionType(DjangoObjectType):
    class Meta:
        model = QuestionInteraction
        fields = [
            "id",
            "session",
            "question_id",
            "serie",
            "time_spent_seconds",
            "revisit_count",
            "order_index",
            "created_at",
        ]


class TrackingEventType(DjangoObjectType):
    class Meta:
        model = TrackingEvent
        fields = ["id", "session", "event_type", "page_url", "metadata", "created_at"]
