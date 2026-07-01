import logging
import time

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Contact, Lead, Formation, FormationRegistration, Service
from .serializers import (
    ContactSerializer, LeadSerializer, FormationSerializer,
    FormationRegistrationSerializer, ServiceSerializer
)


logger = logging.getLogger(__name__)

# Rate limit mémoire volontairement simple : filet applicatif pour petite instance.
# Avec plusieurs workers Gunicorn, plusieurs instances ou montée en charge, s'appuyer sur
# la protection reverse proxy Nginx configurée sur /api/contacts/ ou remplacer par Redis.
CONTACT_RATE_LIMIT = {}
CONTACT_RATE_LIMIT_WINDOW_SECONDS = 10 * 60
CONTACT_RATE_LIMIT_MAX_REQUESTS = 5
CONTACT_MIN_FILL_SECONDS = 3


@api_view(['GET'])
def health_check(request):
    """Retourne un état minimal pour les sondes de disponibilité."""
    return Response({'status': 'ok'})


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['service_type', 'read']
    ordering_fields = ['-created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Créer un contact via le formulaire de contact"""
        if self._is_rate_limited(request):
            return Response(
                {'detail': 'Trop de demandes rapprochées. Réessayez plus tard.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        if request.data.get('website_company'):
            return Response(
                {'detail': 'Merci. Votre demande a bien été reçue.'},
                status=status.HTTP_201_CREATED,
            )

        if self._is_too_fast(request.data.get('started_at')):
            return Response(
                {'detail': 'Merci. Votre demande a bien été reçue.'},
                status=status.HTTP_201_CREATED,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email_error = self._send_contact_email(serializer.validated_data.copy())
        if email_error:
            return Response(
                {'detail': 'La demande n’a pas pu être envoyée pour le moment.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        self.perform_create(serializer)
        return Response(
            {'detail': 'Merci. Votre demande a bien été reçue.'},
            status=status.HTTP_201_CREATED,
        )
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Récupérer les contacts non lus"""
        unread_contacts = self.get_queryset().filter(read=False)
        serializer = self.get_serializer(unread_contacts, many=True)
        return Response(serializer.data)

    def _is_rate_limited(self, request):
        now = time.time()
        client_key = self._client_key(request)
        recent_hits = [
            hit
            for hit in CONTACT_RATE_LIMIT.get(client_key, [])
            if now - hit < CONTACT_RATE_LIMIT_WINDOW_SECONDS
        ]
        CONTACT_RATE_LIMIT[client_key] = recent_hits

        if len(recent_hits) >= CONTACT_RATE_LIMIT_MAX_REQUESTS:
            return True

        recent_hits.append(now)
        return False

    @staticmethod
    def _client_key(request):
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')

    @staticmethod
    def _is_too_fast(started_at):
        try:
            started_at_seconds = int(started_at) / 1000
        except (TypeError, ValueError):
            return True
        return time.time() - started_at_seconds < CONTACT_MIN_FILL_SECONDS

    def _send_contact_email(self, data):
        email_settings = [
            settings.CONTACT_TO,
            settings.CONTACT_FROM,
            settings.EMAIL_HOST,
            settings.EMAIL_PORT,
        ]
        if not all(email_settings):
            logger.warning('Contact email configuration incomplete.')
            return True

        subject = (
            f"[PixelProwlers] Nouvelle demande — "
            f"{data.get('structure_type')} — {data.get('urgency')}"
        )
        body = self._build_email_body(data)

        try:
            EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.CONTACT_FROM,
                to=[settings.CONTACT_TO],
                reply_to=[data.get('email')],
            ).send(fail_silently=False)
        except Exception:
            logger.warning('Contact email delivery failed.', exc_info=False)
            return True

        return False

    @staticmethod
    def _build_email_body(data):
        priority = ContactViewSet._estimate_priority(data)
        lines = [
            'Nouvelle demande PixelProwlers',
            '',
            f"Priorité estimée : {priority}",
            f"Type de structure : {data.get('structure_type')}",
            f"Nom : {data.get('name')}",
            f"Email : {data.get('email')}",
            f"Téléphone : {data.get('phone') or 'Non précisé'}",
            f"Préférence de contact : {data.get('contact_preference')}",
            f"URL du site : {data.get('website_url') or 'Non précisée'}",
            f"CMS : {data.get('cms') or 'Non précisé'}",
            f"Hébergeur : {data.get('hosting') or 'Non précisé'}",
            f"Urgence : {data.get('urgency')}",
            f"Besoin principal : {data.get('service_type')}",
            f"Sauvegardes : {data.get('backups')}",
            f"Accès disponibles : {data.get('access')}",
            f"Budget indicatif : {data.get('budget') or 'Non précisé'}",
            f"Origine déclarative : {data.get('found_us') or 'Non précisée'}",
            '',
            'Message :',
            data.get('message', ''),
            '',
            'Rappel : ne jamais demander ni recevoir de mot de passe, token, clé privée, archive de site ou fichier sensible par email.',
        ]
        return '\n'.join(lines)

    @staticmethod
    def _estimate_priority(data):
        high_signals = {
            'Urgent : activité bloquée',
            'Probablement aucune',
            'Je ne sais pas qui les a',
            'Non',
        }
        if (
            data.get('urgency') in high_signals
            or data.get('backups') in high_signals
            or data.get('access') in high_signals
            or data.get('service_type') == 'urgence'
        ):
            return 'haute'

        qualified_structures = {'Association', 'TPE', 'Indépendant', 'École alternative', 'Collectif'}
        qualified_needs = {'audit_site', 'site_maintenable', 'maintenance_documentation'}
        if (
            data.get('structure_type') in qualified_structures
            and data.get('service_type') in qualified_needs
            and data.get('budget')
            and data.get('contact_preference')
        ):
            return 'normale'

        return 'basse'


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lead_type', 'status', 'timeline']
    ordering_fields = ['-created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Créer un lead depuis le formulaire devis"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Récupérer les leads par type (dev, materiel, formation)"""
        lead_type = request.query_params.get('type')
        if not lead_type:
            return Response({'error': 'type parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        leads = self.get_queryset().filter(lead_type=lead_type)
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data)


class FormationViewSet(viewsets.ModelViewSet):
    queryset = Formation.objects.filter(active=True)
    serializer_class = FormationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['format_type']
    ordering_fields = ['title', 'price']
    
    @action(detail=False, methods=['get'])
    def by_format(self, request):
        """Récupérer les formations par format"""
        format_type = request.query_params.get('format')
        if not format_type:
            return Response({'error': 'format parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        formations = self.get_queryset().filter(format_type=format_type)
        serializer = self.get_serializer(formations, many=True)
        return Response(serializer.data)


class FormationRegistrationViewSet(viewsets.ModelViewSet):
    queryset = FormationRegistration.objects.all()
    serializer_class = FormationRegistrationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['formation', 'status']
    ordering_fields = ['-created_at']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    def create(self, request, *args, **kwargs):
        """Inscrire un utilisateur à une formation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def by_formation(self, request):
        """Récupérer les inscriptions pour une formation"""
        formation_id = request.query_params.get('formation_id')
        if not formation_id:
            return Response({'error': 'formation_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        registrations = self.get_queryset().filter(formation_id=formation_id)
        serializer = self.get_serializer(registrations, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service_category']
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Récupérer les services par catégorie"""
        category = request.query_params.get('category')
        if not category:
            return Response({'error': 'category parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        services = self.get_queryset().filter(service_category=category)
        serializer = self.get_serializer(services, many=True)
        return Response(serializer.data)
