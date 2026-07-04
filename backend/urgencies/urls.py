from django.urls import path

from .views import UrgencyRequestCreateView


urlpatterns = [
    path("urgencies/", UrgencyRequestCreateView.as_view(), name="urgency-create"),
]
