from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewSet, LeadViewSet, FormationViewSet,
    FormationRegistrationViewSet, ServiceViewSet, health_check
)

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'formations', FormationViewSet, basename='formation')
router.register(r'registrations', FormationRegistrationViewSet, basename='registration')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('health/', health_check),
    path('', include(router.urls)),
]
