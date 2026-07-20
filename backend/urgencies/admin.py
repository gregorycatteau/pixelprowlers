from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html

from .models import UrgencyRequest


@admin.register(UrgencyRequest)
class UrgencyRequestAdmin(admin.ModelAdmin):
    list_display = ("reference", "priority_badge", "problem_type", "organization", "contact_preference", "age", "status")
    search_fields = ("reference", "organization", "name", "email", "phone", "affected_url", "short_description")
    list_filter = ("impact_level", "problem_type", "contact_preference", "status", "created_at")
    readonly_fields = (
        "reference", "problem_type", "impact_level", "affected_url", "short_description", "since_when", "name",
        "organization", "email", "phone", "contact_preference", "callback_slot", "expected_next_step",
        "consent_to_contact", "no_secrets_confirmed", "notification_status", "client_dossier", "created_at",
    )
    fieldsets = (
        ("Suivi", {"fields": ("status",)}),
        ("Priorité", {"fields": ("reference", "impact_level", "problem_type", "since_when")}),
        ("Situation", {"fields": ("affected_url", "short_description", "expected_next_step")}),
        ("Contact", {"fields": ("name", "organization", "email", "phone", "contact_preference", "callback_slot")}),
        ("Consentements", {"fields": ("consent_to_contact", "no_secrets_confirmed")}),
        ("Traçabilité", {"fields": ("client_dossier", "notification_status", "created_at")}),
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("client_dossier",)
    list_per_page = 40
    actions = ("mark_in_progress", "mark_resolved")

    @admin.display(description="Priorité", ordering="impact_level")
    def priority_badge(self, obj):
        color = "#f17878" if obj.impact_level in {obj.ImpactLevel.BLOCKED, obj.ImpactLevel.SECURITY_DATA_RISK} else "#f4be5b"
        return format_html('<span style="color:{};font-weight:700">{}</span>', color, obj.get_impact_level_display())

    @admin.display(description="Ancienneté", ordering="created_at")
    def age(self, obj):
        delta = timezone.now() - obj.created_at
        return f"{delta.days} j" if delta.days else f"{max(0, delta.seconds // 3600)} h"

    @admin.action(description="Prendre en charge")
    def mark_in_progress(self, request, queryset):
        updated = queryset.exclude(status="in_progress").update(status="in_progress")
        self.message_user(request, f"{updated} urgence(s) prises en charge.", messages.SUCCESS)

    @admin.action(description="Marquer comme résolues")
    def mark_resolved(self, request, queryset):
        updated = queryset.exclude(status="resolved").update(status="resolved")
        self.message_user(request, f"{updated} urgence(s) résolues.", messages.SUCCESS)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and super().has_delete_permission(request, obj)
