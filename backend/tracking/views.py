import time
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .models import VisitorSession, PageView, QuestionInteraction, TrackingEvent
from .serializers import (
    SessionInitSerializer,
    PageViewSerializer,
    QuestionInteractionSerializer,
    TrackingEventSerializer,
)


class TrackingThrottle(SimpleRateThrottle):
    """
    Simple per-IP rate throttle: 60 requests / minute per IP.
    Adjust 'rate' in settings if needed (TRACKING_THROTTLE_RATE).
    """
    scope = "tracking"
    THROTTLE_RATES = {"tracking": "60/min"}

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return f"throttle_tracking_{ident}"


class SessionInitView(APIView):
    """
    POST /api/tracking/session/init
    Creates a new VisitorSession or returns the existing one if session_id
    already exists. Returns the session_id (UUID) in the response.
    """
    permission_classes = [AllowAny]
    throttle_classes = [TrackingThrottle]

    def post(self, request):
        serializer = SessionInitSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        session_id = serializer.validated_data["session_id"]

        # Try to find existing session
        try:
            session = VisitorSession.objects.get(session_id=session_id)
            # Update last_seen and UTM
            if session.utm_source or session.utm_medium or session.utm_campaign:
                pass  # already set
            serializer.update(session, serializer.validated_data)
        except VisitorSession.DoesNotExist:
            session = serializer.save()

        return Response(
            {"session_id": str(session.session_id), "created": session.created_at.isoformat()},
            status=status.HTTP_200_OK,
        )


class PageViewEndpoint(APIView):
    """
    POST /api/tracking/pageview
    Records a PageView + a linked TrackingEvent (type=pageview) in one call.
    """
    permission_classes = [AllowAny]
    throttle_classes = [TrackingThrottle]

    def post(self, request):
        session = self._get_session(request)
        if session is None:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        url = data.get("url", "")
        title = data.get("title", "")

        page_view = PageView.objects.create(
            session=session,
            url=url,
            title=title or None,
        )
        TrackingEvent.objects.create(
            session=session,
            event_type="pageview",
            page_url=url,
            metadata={"page_title": title} if title else {},
        )

        return Response(
            {"pageview_id": str(page_view.id)},
            status=status.HTTP_201_CREATED,
        )

    def _get_session(self, request):
        session_id = request.data.get("session_id") or request.query_params.get("session_id")
        if not session_id:
            return None
        try:
            return VisitorSession.objects.get(session_id=session_id)
        except VisitorSession.DoesNotExist:
            return None


class QuestionInteractionEndpoint(APIView):
    """
    POST /api/tracking/question-interaction
    Records or updates a QuestionInteraction for the given session.
    If the question_id was already seen for this session, the existing
    record is updated (revisit_count incremented, time_spent updated).
    """
    permission_classes = [AllowAny]
    throttle_classes = [TrackingThrottle]

    def post(self, request):
        session = self._get_session(request)
        if session is None:
            return Response(
                {"error": "session_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuestionInteractionSerializer(
            data=request.data,
            context={"session": session, "request": request},
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        interaction = serializer.save()

        return Response(
            {
                "interaction_id": str(interaction.id),
                "revisit_count": interaction.revisit_count,
            },
            status=status.HTTP_201_CREATED,
        )

    def _get_session(self, request):
        session_id = request.data.get("session_id") or request.query_params.get("session_id")
        if not session_id:
            return None
        try:
            return VisitorSession.objects.get(session_id=session_id)
        except VisitorSession.DoesNotExist:
            return None


class TrackingEventEndpoint(APIView):
    """
    POST /api/tracking/event
    Records a generic TrackingEvent (cta_click, form_submit, form_abandon, custom).
    Use for all non-pageview events sent by the frontend.
    """
    permission_classes = [AllowAny]
    throttle_classes = [TrackingThrottle]

    def post(self, request):
        session = self._get_session(request)

        serializer = TrackingEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event = TrackingEvent.objects.create(
            session=session,
            event_type=serializer.validated_data["event_type"],
            page_url=serializer.validated_data["page_url"],
            metadata=serializer.validated_data.get("metadata", {}),
        )

        return Response(
            {"event_id": str(event.id)},
            status=status.HTTP_201_CREATED,
        )

    def _get_session(self, request):
        session_id = request.data.get("session_id") or request.query_params.get("session_id")
        if not session_id:
            return None
        try:
            return VisitorSession.objects.get(session_id=session_id)
        except VisitorSession.DoesNotExist:
            return None
