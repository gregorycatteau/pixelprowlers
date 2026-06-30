from django.contrib import admin

from .models import Contact, Formation, FormationRegistration, Lead, Service


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'service_type', 'read', 'created_at')
    list_filter = ('service_type', 'read', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company', 'lead_type', 'status', 'created_at')
    list_filter = ('lead_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'company', 'project_description')


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('title', 'format_type', 'duration_hours', 'price', 'active')
    list_filter = ('format_type', 'active')
    search_fields = ('title', 'description')


@admin.register(FormationRegistration)
class FormationRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'formation', 'number_of_participants', 'status', 'created_at')
    list_filter = ('status', 'formation', 'created_at')
    search_fields = ('name', 'email', 'company')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'service_category', 'order')
    list_filter = ('service_category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
