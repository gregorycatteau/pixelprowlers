from django.urls import path

from .views import (
    SessionInitView,
    PageViewEndpoint,
    QuestionInteractionEndpoint,
    TrackingEventEndpoint,
)

app_name = "tracking"

urlpatterns = [
    path("session/init", SessionInitView.as_view(), name="session-init"),
    path("pageview", PageViewEndpoint.as_view(), name="pageview"),
    path("question-interaction", QuestionInteractionEndpoint.as_view(), name="question-interaction"),
    path("event", TrackingEventEndpoint.as_view(), name="event"),
]