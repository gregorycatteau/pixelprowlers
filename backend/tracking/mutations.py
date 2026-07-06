from __future__ import annotations

import graphene
from graphql import GraphQLError

from .models import PageView, QuestionInteraction, TrackingEvent, VisitorSession
from .serializers import (
    PageViewSerializer,
    QuestionInteractionSerializer,
    SessionInitSerializer,
    TrackingEventSerializer,
)
from .types import PageViewType, QuestionInteractionType, TrackingEventType, VisitorSessionType


TRACKING_RATE_LIMIT = 60
TRACKING_RATE_WINDOW_SECONDS = 60


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
        return None

    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR")


def _tracking_cache_key(request) -> str:
    return f"throttle_tracking_{_client_ip(request) or 'unknown'}"


def _check_rate_limit(request) -> bool:
    from django.core.cache import cache

    key = _tracking_cache_key(request)
    count = cache.get(key, 0)
    if count >= TRACKING_RATE_LIMIT:
        return False
    cache.set(key, count + 1, timeout=TRACKING_RATE_WINDOW_SECONDS)
    return True


def _resolve_session(session_id):
    if not session_id:
        return None
    try:
        return VisitorSession.objects.get(session_id=session_id)
    except VisitorSession.DoesNotExist:
        return None


class SessionInit(graphene.Mutation):
    class Arguments:
        session_id = graphene.UUID(required=True)
        referrer = graphene.String(required=False)
        utm_source = graphene.String(required=False)
        utm_medium = graphene.String(required=False)
        utm_campaign = graphene.String(required=False)
        language = graphene.String(required=False)

    session_id = graphene.UUID()
    created = graphene.DateTime()
    session = graphene.Field(VisitorSessionType)

    def mutate(self, info, **kwargs):
        request = _request_from_info(info)
        if not _check_rate_limit(request):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        serializer = SessionInitSerializer(
            data=kwargs,
            context={
                "ip_address": _client_ip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT", "") if request is not None else "",
                "request": request,
            },
        )
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        session_id = serializer.validated_data["session_id"]
        try:
            session = VisitorSession.objects.get(session_id=session_id)
            serializer.update(session, serializer.validated_data)
        except VisitorSession.DoesNotExist:
            session = serializer.save()

        return SessionInit(session_id=session.session_id, created=session.created_at, session=session)


class RecordPageView(graphene.Mutation):
    class Arguments:
        session_id = graphene.UUID(required=True)
        url = graphene.String(required=True)
        title = graphene.String(required=False)

    pageview_id = graphene.UUID()
    page_view = graphene.Field(PageViewType)

    def mutate(self, info, session_id, url, title=None):
        request = _request_from_info(info)
        if not _check_rate_limit(request):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        session = _resolve_session(session_id)
        if session is None:
            raise GraphQLError("session_id is required")

        serializer = PageViewSerializer(data={"url": url, "title": title or None})
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        page_view = PageView.objects.create(session=session, url=url, title=title or None)
        TrackingEvent.objects.create(
            session=session,
            event_type="pageview",
            page_url=url,
            metadata={"page_title": title} if title else {},
        )
        return RecordPageView(pageview_id=page_view.id, page_view=page_view)


class RecordQuestionInteraction(graphene.Mutation):
    class Arguments:
        session_id = graphene.UUID(required=True)
        question_id = graphene.String(required=True)
        serie = graphene.String(required=False)
        time_spent_seconds = graphene.Float(required=False)
        revisit_count = graphene.Int(required=False)
        order_index = graphene.Int(required=False)

    interaction_id = graphene.UUID()
    revisit_count = graphene.Int()
    interaction = graphene.Field(QuestionInteractionType)

    def mutate(self, info, session_id, question_id, serie=None, time_spent_seconds=0.0, revisit_count=0, order_index=0):
        request = _request_from_info(info)
        if not _check_rate_limit(request):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        session = _resolve_session(session_id)
        if session is None:
            raise GraphQLError("session_id is required")

        serializer = QuestionInteractionSerializer(
            data={
                "question_id": question_id,
                "serie": serie,
                "time_spent_seconds": time_spent_seconds,
                "revisit_count": revisit_count,
                "order_index": order_index,
            },
            context={"session": session, "request": request},
        )
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        interaction = serializer.save()
        return RecordQuestionInteraction(
            interaction_id=interaction.id,
            revisit_count=interaction.revisit_count,
            interaction=interaction,
        )


class RecordTrackingEvent(graphene.Mutation):
    class Arguments:
        session_id = graphene.UUID(required=False)
        event_type = graphene.String(required=True)
        page_url = graphene.String(required=True)
        metadata = graphene.JSONString(required=False)

    event_id = graphene.UUID()
    event = graphene.Field(TrackingEventType)

    def mutate(self, info, session_id=None, event_type=None, page_url=None, metadata=None):
        request = _request_from_info(info)
        if not _check_rate_limit(request):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        serializer = TrackingEventSerializer(
            data={
                "event_type": event_type,
                "page_url": page_url,
                "metadata": metadata or {},
            }
        )
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        session = _resolve_session(session_id)
        event = TrackingEvent.objects.create(
            session=session,
            event_type=serializer.validated_data["event_type"],
            page_url=serializer.validated_data["page_url"],
            metadata=serializer.validated_data.get("metadata", {}),
        )
        return RecordTrackingEvent(event_id=event.id, event=event)


class Mutation(graphene.ObjectType):
    session_init = SessionInit.Field()
    record_page_view = RecordPageView.Field()
    record_question_interaction = RecordQuestionInteraction.Field()
    record_tracking_event = RecordTrackingEvent.Field()


class Query(graphene.ObjectType):
    pass
