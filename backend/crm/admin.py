from django.contrib import admin

from .models import Contact, ContactMessage, DiagnosticTicket, Formation, FormationRegistration, Lead, Service


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("ticket_id", "name", "email", "service_type", "status", "read", "created_at")
    list_filter = ("service_type", "demand_type", "status", "read", "created_at")
    search_fields = ("ticket_id", "name", "email", "company")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("contact", "author", "author_name", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("contact__ticket_id", "author_name", "message")


@admin.register(DiagnosticTicket)
class DiagnosticTicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_id", "organization", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("ticket_id", "organization", "email")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "lead_type", "status", "created_at")
    list_filter = ("lead_type", "status", "created_at")
    search_fields = ("name", "email", "company")


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ("title", "format_type", "price", "active")
    list_filter = ("format_type", "active")
    search_fields = ("title",)


@admin.register(FormationRegistration)
class FormationRegistrationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "formation", "status", "created_at")
    list_filter = ("status", "formation", "created_at")
    search_fields = ("name", "email", "company")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "service_category", "order")
    list_filter = ("service_category",)
    search_fields = ("name", "slug")
