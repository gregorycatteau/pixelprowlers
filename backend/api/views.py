from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Contact, Lead, Formation, FormationRegistration, Service
from .serializers import (
    ContactSerializer, LeadSerializer, FormationSerializer,
    FormationRegistrationSerializer, ServiceSerializer
)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Récupérer les contacts non lus"""
        unread_contacts = self.get_queryset().filter(read=False)
        serializer = self.get_serializer(unread_contacts, many=True)
        return Response(serializer.data)


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
