import random
from datetime import datetime

from django.core.cache import cache
from django.db.models import F, Max, Min
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Citation
from .models import Motif, RaisonAppel, RefonteAudit
from .rdv_services import available_slots, calendar_month
from .serializers import (
    AuditDossierCreateSerializer,
    AuditSubmitSerializer,
    CitationSerializer,
    MotifSerializer,
    RaisonAppelSerializer,
    RefonteAuditCreateSerializer,
    RefonteAuditSerializer,
    RdvReservationSerializer,
    RdvSerializer,
)


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_limit_key(request, action: str) -> str:
    return f"audit-{action}-rate:{_client_ip(request)}"


def _check_rate_limit(request, action: str, limit: int) -> bool:
    key = _rate_limit_key(request, action)
    count = cache.get(key, 0)

    if count >= limit:
        return False

    cache.set(key, count + 1, timeout=15 * 60)
    return True


class AuditDossierCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not _check_rate_limit(request, "create", 8):
            return Response(
                {"detail": "Trop de demandes en peu de temps. Réessayez dans quelques minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = AuditDossierCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dossier = serializer.save()

        return Response(
            {
                "numero_dossier": dossier.numero_dossier,
                "statut": dossier.statut,
            },
            status=status.HTTP_201_CREATED,
        )


class AuditSubmitResponsesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not _check_rate_limit(request, "submit", 12):
            return Response(
                {"detail": "Trop de soumissions en peu de temps. Réessayez dans quelques minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = AuditSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reponse = serializer.save()

        return Response(
            {
                "numero_dossier": reponse.dossier.numero_dossier,
                "statut": reponse.dossier.statut,
                "scores_series": reponse.scores_series,
                "score_global": str(reponse.score_global),
                "pilier_faible": reponse.pilier_faible,
                "notification_status": reponse.dossier.notification_status,
            },
            status=status.HTTP_200_OK,
        )


class RandomCitationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exclude_id = request.query_params.get("exclude_id")
        queryset = Citation.objects.filter(actif=True, numero__isnull=False)

        if exclude_id and exclude_id.isdigit() and queryset.count() > 1:
            queryset = queryset.exclude(id=int(exclude_id))

        bounds = queryset.aggregate(min_numero=Min("numero"), max_numero=Max("numero"))
        min_numero = bounds["min_numero"]
        max_numero = bounds["max_numero"]

        citation = None
        if min_numero is not None and max_numero is not None:
            target = random.randint(min_numero, max_numero)
            citation = queryset.filter(numero__gte=target).order_by("numero").first()
            if not citation:
                citation = queryset.order_by("numero").first()

        if not citation:
            return Response(
                {"detail": "Aucune citation active disponible."},
                status=status.HTTP_404_NOT_FOUND,
            )

        Citation.objects.filter(pk=citation.pk).update(nb_affichages=F("nb_affichages") + 1)
        citation.refresh_from_db(fields=["nb_affichages"])

        return Response(CitationSerializer(citation).data, status=status.HTTP_200_OK)


class RefonteAuditCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not _check_rate_limit(request, "refonte-create", 6):
            return Response(
                {"detail": "Trop de demandes en peu de temps. Réessayez dans quelques minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = RefonteAuditCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        audit = serializer.save()

        return Response(
            {
                "reference": audit.reference,
                "analysis_status": audit.analysis_status,
            },
            status=status.HTTP_201_CREATED,
        )


class RefonteAuditDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request, reference: str):
        try:
            audit = RefonteAudit.objects.get(reference=reference)
        except RefonteAudit.DoesNotExist:
            return Response({"detail": "Audit refonte introuvable."}, status=status.HTTP_404_NOT_FOUND)

        return Response(RefonteAuditSerializer(audit).data, status=status.HTTP_200_OK)


class MotifListView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request):
        return Response(MotifSerializer(Motif.objects.filter(actif=True), many=True).data)


class RaisonAppelListView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request):
        return Response(RaisonAppelSerializer(RaisonAppel.objects.filter(actif=True), many=True).data)


class CreneauxDisponiblesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        motif_id = request.query_params.get("motif")
        date_debut = request.query_params.get("date_debut")
        date_fin = request.query_params.get("date_fin")
        urgence = request.query_params.get("urgence") in {"1", "true", "oui"}

        if not motif_id or not date_debut or not date_fin:
            return Response({"detail": "motif, date_debut et date_fin sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            motif = Motif.objects.get(id=int(motif_id), actif=True)
            start_date = datetime.strptime(date_debut, "%Y-%m-%d").date()
            end_date = datetime.strptime(date_fin, "%Y-%m-%d").date()
        except (ValueError, Motif.DoesNotExist):
            return Response({"detail": "Paramètres de disponibilité invalides."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"results": available_slots(motif, start_date, end_date, urgence)})


class CalendrierMoisView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            year = int(request.query_params.get("annee", ""))
            month = int(request.query_params.get("mois", ""))
            if month < 1 or month > 12:
                raise ValueError
        except ValueError:
            return Response({"detail": "annee et mois sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"results": calendar_month(year, month)})


class RdvReserveView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RdvReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rdv = serializer.save()
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)
        return Response(RdvSerializer(rdv).data, status=status.HTTP_201_CREATED)
