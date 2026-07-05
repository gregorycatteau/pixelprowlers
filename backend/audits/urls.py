from django.urls import path

from .views import (
    AuditDossierCreateView,
    AuditSubmitResponsesView,
    CalendrierMoisView,
    CreneauxDisponiblesView,
    MotifListView,
    RaisonAppelListView,
    RandomCitationView,
    RefonteAuditCreateView,
    RefonteAuditDetailView,
    RdvReserveView,
)


urlpatterns = [
    path("audit/creer-dossier/", AuditDossierCreateView.as_view(), name="audit-create-dossier"),
    path("audit/soumettre-reponses/", AuditSubmitResponsesView.as_view(), name="audit-submit-responses"),
    path("audit-refonte/", RefonteAuditCreateView.as_view(), name="refonte-audit-create"),
    path("audit-refonte/<str:reference>/", RefonteAuditDetailView.as_view(), name="refonte-audit-detail"),
    path("citations/random/", RandomCitationView.as_view(), name="citation-random"),
    path("motifs/", MotifListView.as_view(), name="motif-list"),
    path("raisons-appel/", RaisonAppelListView.as_view(), name="raison-appel-list"),
    path("creneaux/disponibles/", CreneauxDisponiblesView.as_view(), name="creneaux-disponibles"),
    path("calendrier/mois/", CalendrierMoisView.as_view(), name="calendrier-mois"),
    path("rdv/reserver/", RdvReserveView.as_view(), name="rdv-reserver"),
]
