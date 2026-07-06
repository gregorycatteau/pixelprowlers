from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import date, timedelta, time

from .models import (
    AuditDossier,
    AuditDossierCounter,
    AuditReponse,
    Citation,
    CreneauCalendrier,
    Motif,
    RaisonAppel,
    RefonteAudit,
    Rdv,
    RdvContact,
    RdvRappel,
)

admin.site.site_header = "PixelProwlers - Administration"
admin.site.site_title = "PixelProwlers Admin"
admin.site.index_title = "Poste de pilotage"


# --- Inlines ---

class AuditReponseInline(admin.StackedInline):
    model = AuditReponse
    extra = 0
    readonly_fields = ("date_soumission",)
    can_delete = False


class RdvRappelInline(admin.TabularInline):
    model = RdvRappel
    extra = 0
    readonly_fields = ("sent_at",)


class CreneauCalendrierInline(admin.TabularInline):
    model = CreneauCalendrier
    extra = 0
    fk_name = "client"  # à adapter selon ton FK réel vers Rdv/RdvContact


# --- AuditDossier ---

@admin.register(AuditDossier)
class AuditDossierAdmin(admin.ModelAdmin):
    list_display = (
        "numero_dossier", "prenom", "nom", "email",
        "type_personne", "statut_badge", "date_creation"
    )
    search_fields = ("numero_dossier", "prenom", "nom", "email", "nom_structure")
    list_filter = ("type_personne", "statut", "date_creation")
    readonly_fields = ("numero_dossier", "date_creation", "notification_status")
    date_hierarchy = "date_creation"
    ordering = ("-date_creation",)
    list_per_page = 30
    inlines = [AuditReponseInline]
    actions = ("marquer_traite", "marquer_en_attente")

    def statut_badge(self, obj):
        colors = {
            "nouveau": "#5bc0de",
            "en_attente": "#f0ad4e",
            "traite": "#5cb85c",
            "annule": "#d9534f",
        }
        color = colors.get(obj.statut, "#999")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:8px;font-size:11px;">{}</span>',
            color, obj.get_statut_display() if hasattr(obj, "get_statut_display") else obj.statut
        )
    statut_badge.short_description = "Statut"

    @admin.action(description="Marquer comme traité")
    def marquer_traite(self, request, queryset):
        updated = queryset.update(statut="traite")
        self.message_user(request, f"{updated} dossier(s) marqué(s) traité(s).")

    @admin.action(description="Remettre en attente")
    def marquer_en_attente(self, request, queryset):
        updated = queryset.update(statut="en_attente")
        self.message_user(request, f"{updated} dossier(s) remis en attente.")


@admin.register(AuditReponse)
class AuditReponseAdmin(admin.ModelAdmin):
    list_display = ("dossier", "score_global", "pilier_faible", "date_soumission")
    search_fields = ("dossier__numero_dossier", "dossier__email")
    list_filter = ("pilier_faible", "date_soumission")
    readonly_fields = ("date_soumission",)
    date_hierarchy = "date_soumission"


@admin.register(AuditDossierCounter)
class AuditDossierCounterAdmin(admin.ModelAdmin):
    list_display = ("year", "last_number")
    readonly_fields = ("year", "last_number")

    def has_add_permission(self, request):
        # Généralement auto-généré, on évite les créations manuelles hasardeuses
        return False


# --- RefonteAudit ---

@admin.register(RefonteAudit)
class RefonteAuditAdmin(admin.ModelAdmin):
    list_display = (
        "reference", "prenom", "nom", "email", "site_url",
        "status_badge", "date_creation"
    )
    search_fields = ("reference", "prenom", "nom", "email", "nom_structure", "site_url")
    list_filter = ("analysis_status", "type_personne", "date_creation")
    date_hierarchy = "date_creation"
    ordering = ("-date_creation",)
    readonly_fields = (
        "reference",
        "reponses",
        "technical_report",
        "pagespeed_report",
        "heuristic_report",
        "analysis_error",
        "date_creation",
        "date_maj",
    )

    def status_badge(self, obj):
        colors = {
            "pending": "#f0ad4e",
            "running": "#5bc0de",
            "done": "#5cb85c",
            "error": "#d9534f",
        }
        color = colors.get(obj.analysis_status, "#999")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:8px;font-size:11px;">{}</span>',
            color, obj.analysis_status
        )
    status_badge.short_description = "Analyse"


# --- Citation ---

@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = (
        "numero", "auteur", "source", "annee", "langue",
        "theme", "actif", "verifie", "nb_affichages", "date_creation"
    )
    search_fields = ("texte", "auteur", "source")
    list_filter = ("actif", "verifie", "langue", "theme", "annee", "auteur", "date_creation")
    readonly_fields = ("date_creation", "date_maj", "nb_affichages")
    list_editable = ("actif", "verifie")
    ordering = ("-date_creation",)
    actions = ("marquer_verifie", "activer", "desactiver")

    @admin.action(description="Marquer comme vérifiées")
    def marquer_verifie(self, request, queryset):
        queryset.update(verifie=True)

    @admin.action(description="Activer les citations sélectionnées")
    def activer(self, request, queryset):
        queryset.update(actif=True)

    @admin.action(description="Désactiver les citations sélectionnées")
    def desactiver(self, request, queryset):
        queryset.update(actif=False)


# --- Motif / RaisonAppel ---

@admin.register(Motif)
class MotifAdmin(admin.ModelAdmin):
    list_display = ("nom", "duree_minutes", "creneau_type", "actif", "ordre")
    list_filter = ("actif", "creneau_type")
    search_fields = ("nom",)
    list_editable = ("actif", "ordre")
    ordering = ("ordre",)


@admin.register(RaisonAppel)
class RaisonAppelAdmin(admin.ModelAdmin):
    list_display = ("nom", "actif", "ordre")
    list_filter = ("actif",)
    search_fields = ("nom",)
    list_editable = ("actif", "ordre")
    ordering = ("ordre",)


# --- RdvContact ---

@admin.register(RdvContact)
class RdvContactAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email", "telephone", "nb_rdv", "updated_at")
    search_fields = ("prenom", "nom", "email", "telephone")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)

    def nb_rdv(self, obj):
        return obj.rdv_set.count() if hasattr(obj, "rdv_set") else "-"
    nb_rdv.short_description = "Nb RDV"


# --- CreneauCalendrier ---

@admin.register(CreneauCalendrier)
class CreneauCalendrierAdmin(admin.ModelAdmin):
    list_display = (
        "date", "heure_debut", "heure_fin", "statut_badge",
        "motif_reserve", "urgence", "client"
    )
    list_filter = ("statut", "urgence", "date", "motif_reserve")
    search_fields = ("client__email", "client__nom", "motif_reserve__nom")
    date_hierarchy = "date"
    ordering = ("date", "heure_debut")
    actions = ("create_standard_two_weeks", "mark_blocked", "mark_free")

    def statut_badge(self, obj):
        colors = {
            CreneauCalendrier.Statut.LIBRE: "#5cb85c",
            CreneauCalendrier.Statut.RESERVE: "#f0ad4e",
            CreneauCalendrier.Statut.BLOQUE: "#d9534f",
        }
        color = colors.get(obj.statut, "#999")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:8px;font-size:11px;">{}</span>',
            color, obj.get_statut_display()
        )
    statut_badge.short_description = "Statut"

    @admin.action(description="Créer les créneaux libres standards sur 2 semaines")
    def create_standard_two_weeks(self, request, queryset):
        today = date.today()
        created = 0
        for day_offset in range(14):
            current = today + timedelta(days=day_offset)
            if current.weekday() >= 5:
                continue
            for start, end in [(time(9, 0), time(12, 30)), (time(14, 0), time(18, 0))]:
                _, was_created = CreneauCalendrier.objects.get_or_create(
                    date=current, heure_debut=start, heure_fin=end
                )
                created += int(was_created)
        self.message_user(request, f"{created} créneau(x) créé(s).")

    @admin.action(description="Bloquer les créneaux sélectionnés")
    def mark_blocked(self, request, queryset):
        updated = queryset.update(statut=CreneauCalendrier.Statut.BLOQUE)
        self.message_user(request, f"{updated} créneau(x) bloqué(s).")

    @admin.action(description="Libérer les créneaux sélectionnés")
    def mark_free(self, request, queryset):
        updated = queryset.update(
            statut=CreneauCalendrier.Statut.LIBRE, motif_reserve=None, client=None
        )
        self.message_user(request, f"{updated} créneau(x) libéré(s).")


# --- Rdv ---

@admin.register(Rdv)
class RdvAdmin(admin.ModelAdmin):
    list_display = ("contact", "motif", "urgence", "statut_badge", "created_at")
    list_filter = ("motif", "urgence", "statut", "created_at")
    search_fields = ("contact__email", "contact__nom", "contact__prenom")
    readonly_fields = ("notification_status", "created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    inlines = [RdvRappelInline]
    actions = ("marquer_confirme", "marquer_annule")

    def statut_badge(self, obj):
        colors = {
            "en_attente": "#f0ad4e",
            "confirme": "#5cb85c",
            "annule": "#d9534f",
            "termine": "#5bc0de",
        }
        color = colors.get(obj.statut, "#999")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:8px;font-size:11px;">{}</span>',
            color, obj.statut
        )
    statut_badge.short_description = "Statut"

    @admin.action(description="Marquer comme confirmé")
    def marquer_confirme(self, request, queryset):
        updated = queryset.update(statut="confirme")
        self.message_user(request, f"{updated} RDV confirmé(s).")

    @admin.action(description="Marquer comme annulé")
    def marquer_annule(self, request, queryset):
        updated = queryset.update(statut="annule")
        self.message_user(request, f"{updated} RDV annulé(s).")


@admin.register(RdvRappel)
class RdvRappelAdmin(admin.ModelAdmin):
    list_display = ("rdv", "type_rappel", "scheduled_at", "status", "sent_at")
    list_filter = ("type_rappel", "status", "scheduled_at")
    date_hierarchy = "scheduled_at"
    ordering = ("scheduled_at",)
