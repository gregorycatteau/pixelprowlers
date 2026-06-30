from rest_framework import serializers
from .models import Contact, Lead, Formation, FormationRegistration, Service


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'company', 'phone', 'service_type', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


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
