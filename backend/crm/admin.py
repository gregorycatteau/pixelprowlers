from django.contrib import admin, messages
from django.utils.html import format_html

from .models import Contact, ContactDailyCounter, ContactMessage, DiagnosticTicket, Formation, FormationRegistration, Lead, Service


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("numero_dossier", "customer_name", "demand_badge", "status_badge", "statut_notification", "read", "date_creation")
    list_filter = ("service_type", "demand_type", "status", "statut_notification", "read", "date_creation")
    search_fields = ("numero_dossier", "ticket_id", "nom", "prenom", "name", "email", "company", "phone")
    readonly_fields = (
        "ticket_id", "secret_token", "numero_dossier", "nom", "prenom", "name", "email", "company", "phone",
        "service_type", "demand_type", "objet", "methode_contact", "message", "date_creation", "signature_hmac",
        "notification_status", "statut_notification", "date_notification", "created_at", "updated_at", "client_dossier",
    )
    fieldsets = (
        ("Traitement", {"fields": ("status", "read")}),
        ("Demande", {"fields": ("numero_dossier", "service_type", "demand_type", "objet", "message")}),
        ("Contact", {"fields": ("nom", "prenom", "name", "email", "company", "phone", "methode_contact")}),
        ("Dossier", {"fields": ("client_dossier", "ticket_id", "date_creation", "created_at", "updated_at")}),
        ("Notification", {"fields": ("statut_notification", "date_notification", "notification_status")}),
        ("Données protégées", {"fields": ("secret_token", "signature_hmac"), "classes": ("collapse",)}),
    )
    ordering = ("-date_creation",)
    date_hierarchy = "date_creation"
    list_select_related = ("client_dossier",)
    list_per_page = 40
    actions = ("mark_in_progress", "mark_resolved", "mark_read")

    @admin.display(description="Contact", ordering="nom")
    def customer_name(self, obj):
        return f"{obj.prenom} {obj.nom}".strip() or obj.name

    @admin.display(description="Demande", ordering="demand_type")
    def demand_badge(self, obj):
        color = "#39d0d8" if obj.demand_type == Contact.DemandType.MATERIEL else "#7d8ca3"
        return format_html('<span style="border-left:4px solid {};padding-left:.5rem">{}</span>', color, obj.get_demand_type_display())

    @admin.display(description="Statut", ordering="status")
    def status_badge(self, obj):
        colors = {Contact.Status.OPEN: "#f4be5b", Contact.Status.IN_PROGRESS: "#39d0d8", Contact.Status.RESOLVED: "#67d99a", Contact.Status.CLOSED: "#7d8ca3"}
        return format_html('<span style="color:{};font-weight:700">{}</span>', colors.get(obj.status, "#fff"), obj.get_status_display())

    def _update_status(self, request, queryset, status, label):
        updated = queryset.exclude(status=status).update(status=status)
        self.message_user(request, f"{updated} contact(s) {label}.", messages.SUCCESS)

    @admin.action(description="Prendre en charge")
    def mark_in_progress(self, request, queryset):
        self._update_status(request, queryset, Contact.Status.IN_PROGRESS, "pris en charge")

    @admin.action(description="Marquer comme résolus")
    def mark_resolved(self, request, queryset):
        self._update_status(request, queryset, Contact.Status.RESOLVED, "résolus")

    @admin.action(description="Marquer comme lus")
    def mark_read(self, request, queryset):
        updated = queryset.filter(read=False).update(read=True)
        self.message_user(request, f"{updated} contact(s) marqués comme lus.", messages.SUCCESS)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_delete_permission(request, obj)


@admin.register(ContactDailyCounter)
class ContactDailyCounterAdmin(admin.ModelAdmin):
    list_display = ("date", "value", "updated_at")
    readonly_fields = ("date", "value", "updated_at")
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("contact", "author", "author_name", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("contact__ticket_id", "contact__numero_dossier", "author_name", "message")
    raw_id_fields = ("contact",)
    date_hierarchy = "created_at"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("contact", "author", "author_name", "message", "created_at", "updated_at")
        return ("author", "author_name", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = ContactMessage.Author.SUPPORT
            obj.author_name = request.user.get_username()
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


@admin.register(DiagnosticTicket)
class DiagnosticTicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_id", "organization", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("ticket_id", "organization", "email")
    readonly_fields = ("ticket_id", "organization", "email", "phone", "message", "answers", "diagnostic_result", "email_confirmation", "client_dossier", "created_at", "updated_at")
    date_hierarchy = "created_at"
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "lead_type", "status", "created_at")
    list_filter = ("lead_type", "status", "created_at")
    search_fields = ("name", "email", "company")
    readonly_fields = ("name", "email", "company", "phone", "budget", "project_description", "timeline", "lead_type", "client_dossier", "created_at", "updated_at")
    date_hierarchy = "created_at"
    def has_delete_permission(self, request, obj=None): return request.user.is_superuser


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
    readonly_fields = ("name", "email", "company", "phone", "formation", "client_dossier", "created_at", "updated_at")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "service_category", "order")
    list_filter = ("service_category",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
