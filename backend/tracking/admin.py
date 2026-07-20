from django.contrib import admin

from .models import PageView, QuestionInteraction, TrackingEvent, VisitorSession


class ReadOnlyTrackingAdmin(admin.ModelAdmin):
    actions = None
    list_per_page = 50
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False


@admin.register(VisitorSession)
class VisitorSessionAdmin(ReadOnlyTrackingAdmin):
    list_display = ("session_id", "device_type", "browser", "os", "utm_source", "created_at", "last_seen_at")
    list_filter = ("device_type", "browser", "os", "created_at")
    search_fields = ("session_id", "utm_source", "utm_medium", "utm_campaign")
    readonly_fields = ("id", "session_id", "ip_address", "user_agent", "device_type", "browser", "os", "referrer", "utm_source", "utm_medium", "utm_campaign", "language", "client_dossier", "created_at", "last_seen_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)


@admin.register(PageView)
class PageViewAdmin(ReadOnlyTrackingAdmin):
    list_display = ("id", "session", "url", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("session__session_id", "url", "title")
    readonly_fields = ("id", "session", "url", "title", "created_at")
    date_hierarchy = "created_at"
    list_select_related = ("session",)


@admin.register(QuestionInteraction)
class QuestionInteractionAdmin(ReadOnlyTrackingAdmin):
    list_display = ("id", "session", "question_id", "serie", "time_spent_seconds", "revisit_count", "order_index", "created_at")
    list_filter = ("created_at", "serie")
    search_fields = ("session__session_id", "question_id")
    readonly_fields = ("id", "session", "question_id", "serie", "time_spent_seconds", "revisit_count", "order_index", "created_at")
    date_hierarchy = "created_at"
    list_select_related = ("session",)


@admin.register(TrackingEvent)
class TrackingEventAdmin(ReadOnlyTrackingAdmin):
    list_display = ("id", "session", "event_type", "page_url", "created_at")
    list_filter = ("event_type", "created_at")
    search_fields = ("session__session_id", "page_url")
    readonly_fields = ("id", "session", "event_type", "page_url", "metadata", "created_at")
    date_hierarchy = "created_at"
    list_select_related = ("session",)
