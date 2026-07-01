import re

from rest_framework import serializers
from .models import Contact, Lead, Formation, FormationRegistration, Service


class ContactSerializer(serializers.ModelSerializer):
    STRUCTURE_TYPES = {
        'Association',
        'TPE',
        'Indépendant',
        'École alternative',
        'Collectif',
        'Autre petite structure',
    }
    SERVICE_TYPES = {
        'audit_site',
        'site_maintenable',
        'maintenance_documentation',
        'materiel',
        'formation',
        'urgence',
        'autre',
    }
    URGENCY_LEVELS = {
        'Urgent : activité bloquée',
        'À traiter rapidement',
        'Prévention / diagnostic',
        'Projet à cadrer',
    }
    CONTACT_PREFERENCES = {
        'Email',
        'Téléphone',
        'Email puis appel si nécessaire',
    }
    BACKUP_STATUSES = {
        'Oui, restauration déjà testée',
        'Oui, mais jamais testée',
        'Je ne sais pas',
        'Probablement aucune',
    }
    ACCESS_STATUSES = {
        'Oui, accès admin et hébergement',
        'Accès partiels',
        'Je ne sais pas qui les a',
        'Non',
    }
    BUDGETS = {
        '',
        'Moins de 500 €',
        '500 à 1 500 €',
        '1 500 à 4 000 €',
        'Plus de 4 000 €',
        'À cadrer ensemble',
    }
    FOUND_US_CHOICES = {
        '',
        'Recherche web',
        'Bouche-à-oreille',
        'Réseau local',
        'Ressources PixelProwlers',
        'Autre',
    }
    CMS_CHOICES = {'', 'WordPress', 'Prestashop', 'Drupal', 'Site statique', 'Nuxt / Vue', 'Autre'}

    structure_type = serializers.CharField(write_only=True, max_length=80)
    urgency = serializers.CharField(write_only=True, max_length=80)
    contact_preference = serializers.CharField(write_only=True, max_length=80)
    website_url = serializers.URLField(write_only=True, required=False, allow_blank=True, max_length=240)
    cms = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=80)
    hosting = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=120)
    backups = serializers.CharField(write_only=True, max_length=80)
    access = serializers.CharField(write_only=True, max_length=80)
    budget = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=80)
    found_us = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=80)
    privacy_consent = serializers.BooleanField(write_only=True)
    website_company = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=120)
    started_at = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Contact
        fields = [
            'id',
            'name',
            'email',
            'company',
            'phone',
            'service_type',
            'message',
            'created_at',
            'structure_type',
            'urgency',
            'contact_preference',
            'website_url',
            'cms',
            'hosting',
            'backups',
            'access',
            'budget',
            'found_us',
            'privacy_consent',
            'website_company',
            'started_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        attrs = self._strip_values(attrs)
        self._validate_single_line_fields(attrs)
        self._validate_choice('structure_type', attrs.get('structure_type'), self.STRUCTURE_TYPES)
        self._validate_choice('service_type', attrs.get('service_type'), self.SERVICE_TYPES)
        self._validate_choice('urgency', attrs.get('urgency'), self.URGENCY_LEVELS)
        self._validate_choice('contact_preference', attrs.get('contact_preference'), self.CONTACT_PREFERENCES)
        self._validate_choice('backups', attrs.get('backups'), self.BACKUP_STATUSES)
        self._validate_choice('access', attrs.get('access'), self.ACCESS_STATUSES)
        self._validate_choice('budget', attrs.get('budget', ''), self.BUDGETS)
        self._validate_choice('found_us', attrs.get('found_us', ''), self.FOUND_US_CHOICES)
        self._validate_choice('cms', attrs.get('cms', ''), self.CMS_CHOICES)

        if len(attrs.get('name', '')) < 2:
            raise serializers.ValidationError({'name': 'Indiquez au moins 2 caractères.'})
        if len(attrs.get('message', '')) < 20:
            raise serializers.ValidationError({'message': 'Décrivez la situation en au moins 20 caractères.'})
        if len(attrs.get('message', '')) > 4000:
            raise serializers.ValidationError({'message': 'Le message est trop long.'})
        if not attrs.get('privacy_consent'):
            raise serializers.ValidationError({'privacy_consent': 'Le consentement est requis.'})
        if attrs.get('phone') and not re.fullmatch(r"[0-9+().\s-]{6,30}", attrs['phone']):
            raise serializers.ValidationError({'phone': 'Numéro de téléphone invalide.'})

        return attrs

    def create(self, validated_data):
        contact_fields = {
            field: validated_data.pop(field, '')
            for field in [
                'structure_type',
                'urgency',
                'contact_preference',
                'website_url',
                'cms',
                'hosting',
                'backups',
                'access',
                'budget',
                'found_us',
                'privacy_consent',
                'website_company',
                'started_at',
            ]
        }
        validated_data['message'] = self._build_stored_message(validated_data['message'], contact_fields)
        return super().create(validated_data)

    def to_internal_value(self, data):
        unexpected_fields = set(data.keys()) - set(self.fields.keys())
        if unexpected_fields:
            raise serializers.ValidationError({
                'non_field_errors': 'Certains champs envoyés ne sont pas attendus.'
            })
        return super().to_internal_value(data)

    @staticmethod
    def _strip_values(attrs):
        return {
            key: value.strip() if isinstance(value, str) else value
            for key, value in attrs.items()
        }

    @staticmethod
    def _validate_choice(field_name, value, choices):
        if value not in choices:
            raise serializers.ValidationError({field_name: 'Valeur non reconnue.'})

    @staticmethod
    def _validate_single_line_fields(attrs):
        single_line_fields = {
            'name',
            'email',
            'company',
            'phone',
            'structure_type',
            'service_type',
            'urgency',
            'contact_preference',
            'website_url',
            'cms',
            'hosting',
            'backups',
            'access',
            'budget',
            'found_us',
        }
        for field in single_line_fields:
            value = attrs.get(field)
            if isinstance(value, str) and any(char in value for char in ('\r', '\n')):
                raise serializers.ValidationError({field: 'Valeur invalide.'})

    @staticmethod
    def _build_stored_message(message, fields):
        details = [
            f"Type de structure : {fields.get('structure_type') or 'Non précisé'}",
            f"Urgence : {fields.get('urgency') or 'Non précisée'}",
            f"Préférence de contact : {fields.get('contact_preference') or 'Non précisée'}",
            f"URL du site : {fields.get('website_url') or 'Non précisée'}",
            f"CMS : {fields.get('cms') or 'Non précisé'}",
            f"Hébergeur : {fields.get('hosting') or 'Non précisé'}",
            f"Sauvegardes : {fields.get('backups') or 'Non précisé'}",
            f"Accès disponibles : {fields.get('access') or 'Non précisé'}",
            f"Budget indicatif : {fields.get('budget') or 'Non précisé'}",
            f"Origine déclarative : {fields.get('found_us') or 'Non précisée'}",
        ]
        return f"{chr(10).join(details)}\n\nSituation décrite :\n{message}"


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'email', 'company', 'phone', 'budget', 'project_description', 'timeline', 'lead_type', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ['id', 'title', 'description', 'format_type', 'duration_hours', 'price', 'max_participants', 'scheduled_dates', 'active']
        read_only_fields = ['id']


class FormationRegistrationSerializer(serializers.ModelSerializer):
    formation_title = serializers.CharField(source='formation.title', read_only=True)
    
    class Meta:
        model = FormationRegistration
        fields = ['id', 'formation', 'formation_title', 'name', 'email', 'company', 'phone', 'number_of_participants', 'special_needs', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'slug', 'description', 'icon', 'service_category', 'order']
        read_only_fields = ['id']
