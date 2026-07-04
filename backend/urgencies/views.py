from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UrgencyRequestSerializer
from .services import notify_urgency


def _client_ip(request) -> str:
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _rate_limit_key(request) -> str:
    return f"urgency-rate:{_client_ip(request)}"


@method_decorator(csrf_protect, name="dispatch")
class UrgencyRequestCreateView(APIView):
    permission_classes = [AllowAny]

    # Limite les abus sans journaliser les champs libres du visiteur.
    def _check_rate_limit(self, request) -> bool:
        key = _rate_limit_key(request)
        count = cache.get(key, 0)

        if count >= 5:
            return False

        cache.set(key, count + 1, timeout=15 * 60)
        return True

    def post(self, request):
        if not self._check_rate_limit(request):
            return Response(
                {"detail": "Trop de demandes en peu de temps. Réessayez dans quelques minutes."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = UrgencyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        ticket.notification_status = notify_urgency(ticket)
        ticket.save(update_fields=["notification_status"])

        return Response(
            {
                "reference": ticket.reference,
                "status": ticket.status,
                "message": "Demande urgente enregistrée.",
                "client_email_status": ticket.notification_status.get("client_email", "not_configured"),
            },
            status=status.HTTP_201_CREATED,
        )
