from django.contrib import admin
from django import forms

from .models import Contact, ContactMessage, DiagnosticTicket, Formation, FormationRegistration, Lead, Service, Notification
from .operator_services import reply_to_contact


class ContactOperatorForm(forms.ModelForm):
    reply = forms.CharField(label="Réponse de l’atelier", required=False, max_length=2000,
                           widget=forms.Textarea, help_text="Enregistrée dans le suivi ; notification mise en file privée.")
    class Meta:
        model = Contact
        fields = "__all__"
        exclude = ("secret_token",)


class MessageHistory(admin.TabularInline):
    model = ContactMessage
    fields = ("created_at", "author", "author_name", "message")
    readonly_fields = fields
    ordering = ("created_at", "pk")
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactOperatorForm
    inlines = (MessageHistory,)
    readonly_fields = ("ticket_id", "name", "email", "company", "phone", "service_type", "demand_type", "message", "request_context", "notification_status", "client_dossier", "created_at", "updated_at")
    list_display = ("ticket_id", "name", "email", "besoin", "status", "read", "created_at")
    list_filter = ("service_type", "demand_type", "status", "read", "created_at")
    search_fields = ("ticket_id", "name", "email", "company")

    @admin.display(description="Besoin")
    def besoin(self, obj):
        labels = {"reparation": "Réparation", "reemploi": "Réemploi", "conseil": "Conseil / cybersécurité", "developpement": "Développement", "formation": "Formation", "autre": "Contact"}
        return labels.get(obj.request_context.get("need")) or obj.get_demand_type_display() or obj.get_service_type_display()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.has_perm("crm.add_contactmessage"):
            form.base_fields.pop("reply", None)
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if form.cleaned_data.get("reply"):
            reply_to_contact(contact=obj, message=form.cleaned_data["reply"], operator=request.user)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    readonly_fields = ("contact", "author", "author_name", "message", "created_at", "updated_at")
    list_display = ("contact", "author", "author_name", "created_at")
    list_filter = ("author", "created_at")
    search_fields = ("contact__ticket_id", "author_name", "message")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "event_key", "state", "attempts", "next_attempt_at", "accepted_at", "last_error")
    list_filter = ("state", "created_at")
    search_fields = ("event_key",)
    exclude = ("body",)
    readonly_fields = ("event_key", "recipient", "subject", "sender", "reply_to", "state", "attempts", "next_attempt_at", "lease_until", "accepted_at", "last_error", "created_at", "updated_at")
    actions = ("retry_failures",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Reprendre les échecs sélectionnés (exclut les résultats incertains)", permissions=["change"])
    def retry_failures(self, request, queryset):
        from .outbox import retry
        count = 0
        for item in queryset.filter(state__in=[Notification.State.TEMPORARY, Notification.State.PERMANENT]):
            retry(item.pk)
            count += 1
        self.message_user(request, f"{count} reprise(s) ciblée(s) enregistrée(s). Aucun email envoyé par cette action.")


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
