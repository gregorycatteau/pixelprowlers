from django.contrib import admin

from .models import UrgencyRequest


@admin.register(UrgencyRequest)
class UrgencyRequestAdmin(admin.ModelAdmin):
    list_display = ("reference", "problem_type", "impact_level", "organization", "created_at", "status")
    search_fields = ("reference", "organization", "email", "affected_url")
    list_filter = ("problem_type", "impact_level", "status", "created_at")
    readonly_fields = ("reference", "created_at", "notification_status")
