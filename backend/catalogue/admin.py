from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .models import RefurbishedMachine


@admin.register(RefurbishedMachine)
class RefurbishedMachineAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "brand_model",
        "editorial_badge",
        "commercial_badge",
        "display_price",
        "featured",
        "display_order",
        "updated_at",
    )
    search_fields = ("internal_reference", "title", "brand", "model_name", "slug")
    list_filter = (
        "status",
        "commercial_status",
        "brand",
        "featured",
        "published_at",
        "updated_at",
    )
    date_hierarchy = "updated_at"
    ordering = ("-featured", "display_order", "-published_at", "id")
    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "published_at",
        "archived_at",
        "reserved_at",
        "sold_at",
    )
    fieldsets = (
        ("Identité", {"fields": ("internal_reference", "slug", "title", "brand", "model_name")}),
        ("Présentation", {"fields": ("summary", "description", "cosmetic_condition", "installed_operating_system")}),
        ("Caractéristiques", {"fields": ("specifications",)}),
        ("Interventions et tests", {"fields": ("performed_interventions", "performed_tests", "internal_notes")}),
        ("Disponibilité", {"fields": ("commercial_status", "availability_note", "available_since", "reserved_at", "sold_at")}),
        ("Prix", {"fields": ("price_amount", "currency", "warranty_information")}),
        ("SEO", {"fields": ("seo_title", "seo_description")}),
        ("Publication", {"fields": ("status", "featured", "display_order", "published_at", "archived_at")}),
        ("Traçabilité", {"fields": ("created_at", "updated_at", "created_by", "updated_by")}),
    )
    actions = ("publish_selected", "archive_selected", "mark_available", "mark_reserved", "mark_sold")
    list_select_related = ("created_by", "updated_by")
    list_per_page = 40

    @admin.display(description="Marque / modèle", ordering="brand")
    def brand_model(self, obj):
        return f"{obj.brand} {obj.model_name}".strip()

    @admin.display(description="Publication", ordering="status")
    def editorial_badge(self, obj):
        colors = {obj.Status.DRAFT: "#f4be5b", obj.Status.PUBLISHED: "#67d99a", obj.Status.ARCHIVED: "#7d8ca3"}
        return format_html('<span style="color:{};font-weight:700">{}</span>', colors[obj.status], obj.get_status_display())

    @admin.display(description="Disponibilité", ordering="commercial_status")
    def commercial_badge(self, obj):
        colors = {obj.CommercialStatus.AVAILABLE: "#67d99a", obj.CommercialStatus.RESERVED: "#f4be5b", obj.CommercialStatus.SOLD: "#39d0d8", obj.CommercialStatus.ARCHIVED: "#7d8ca3"}
        return format_html('<span style="color:{};font-weight:700">{}</span>', colors[obj.commercial_status], obj.get_commercial_status_display())

    @admin.display(description="Prix", ordering="price_amount")
    def display_price(self, obj):
        return f"{obj.price_amount:.2f} {obj.currency}" if obj.price_amount is not None else "Sur demande"

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    def get_readonly_fields(self, request, obj=None):
        fields = list(self.readonly_fields)
        if obj and not request.user.is_superuser:
            fields.append("internal_reference")
        if obj and obj.status in {obj.Status.PUBLISHED, obj.Status.ARCHIVED}:
            fields.append("slug")
        if not request.user.has_perm("catalogue.change_refurbishedmachine_commercial_status"):
            fields.extend(("commercial_status", "available_since"))
        return tuple(dict.fromkeys(fields))

    def get_form(self, request, obj=None, **kwargs):
        if obj is not None:
            obj._allow_internal_reference_change = request.user.is_superuser
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        base = super().has_change_permission(request, obj)
        if not base or obj is None or request.user.is_superuser:
            return base
        if obj.status == obj.Status.DRAFT:
            return request.user.has_perm("catalogue.edit_refurbishedmachine_drafts")
        return request.user.has_perm("catalogue.publish_refurbishedmachine")

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    def has_publish_permission(self, request):
        return request.user.is_superuser or request.user.has_perm("catalogue.publish_refurbishedmachine")

    def has_commercial_permission(self, request):
        return request.user.is_superuser or request.user.has_perm(
            "catalogue.change_refurbishedmachine_commercial_status"
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj._allow_internal_reference_change = request.user.is_superuser
        obj.save()

    def _run_transition(self, request, queryset, method_name, success_label):
        changed = unchanged = invalid = 0
        for machine in queryset:
            try:
                if getattr(machine, method_name)():
                    changed += 1
                else:
                    unchanged += 1
            except ValidationError:
                invalid += 1
        level = messages.WARNING if invalid else messages.SUCCESS
        self.message_user(
            request,
            f"{changed} machine(s) {success_label}; {unchanged} déjà dans cet état; {invalid} refusée(s) par la validation.",
            level=level,
        )

    @admin.action(description="Publier les machines sélectionnées", permissions=["publish"])
    def publish_selected(self, request, queryset):
        self._run_transition(request, queryset, "publish", "publiée(s)")

    @admin.action(description="Archiver les machines sélectionnées", permissions=["publish"])
    def archive_selected(self, request, queryset):
        self._run_transition(request, queryset, "archive", "archivée(s)")

    @admin.action(description="Marquer comme disponibles", permissions=["commercial"])
    def mark_available(self, request, queryset):
        self._run_transition(request, queryset, "mark_available", "rendue(s) disponible(s)")

    @admin.action(description="Marquer comme réservées", permissions=["commercial"])
    def mark_reserved(self, request, queryset):
        self._run_transition(request, queryset, "mark_reserved", "réservée(s)")

    @admin.action(description="Marquer comme vendues", permissions=["commercial"])
    def mark_sold(self, request, queryset):
        self._run_transition(request, queryset, "mark_sold", "vendue(s)")
