from django.contrib import admin
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


@admin.register(AuditDossier)
class AuditDossierAdmin(admin.ModelAdmin):
    list_display = ("numero_dossier", "prenom", "nom", "email", "type_personne", "statut", "date_creation")
    search_fields = ("numero_dossier", "prenom", "nom", "email", "nom_structure")
    list_filter = ("type_personne", "statut", "date_creation")
    readonly_fields = ("numero_dossier", "date_creation", "notification_status")


@admin.register(AuditReponse)
class AuditReponseAdmin(admin.ModelAdmin):
    list_display = ("dossier", "score_global", "pilier_faible", "date_soumission")
    search_fields = ("dossier__numero_dossier", "dossier__email")
    list_filter = ("pilier_faible", "date_soumission")
    readonly_fields = ("date_soumission",)


@admin.register(AuditDossierCounter)
class AuditDossierCounterAdmin(admin.ModelAdmin):
    list_display = ("year", "last_number")
    readonly_fields = ("year", "last_number")


@admin.register(RefonteAudit)
class RefonteAuditAdmin(admin.ModelAdmin):
    list_display = ("reference", "prenom", "nom", "email", "site_url", "analysis_status", "date_creation")
    search_fields = ("reference", "prenom", "nom", "email", "nom_structure", "site_url")
    list_filter = ("analysis_status", "type_personne", "date_creation")
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


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    list_display = ("numero", "auteur", "source", "annee", "langue", "theme", "actif", "verifie", "nb_affichages", "date_creation")
    search_fields = ("texte", "auteur", "source")
    list_filter = ("actif", "verifie", "langue", "theme", "annee", "auteur", "date_creation")
    readonly_fields = ("date_creation", "date_maj")


@admin.register(Motif)
class MotifAdmin(admin.ModelAdmin):
    list_display = ("nom", "duree_minutes", "creneau_type", "actif", "ordre")
    list_filter = ("actif", "creneau_type")
    search_fields = ("nom",)


@admin.register(RaisonAppel)
class RaisonAppelAdmin(admin.ModelAdmin):
    list_display = ("nom", "actif", "ordre")
    list_filter = ("actif",)
    search_fields = ("nom",)


@admin.register(RdvContact)
class RdvContactAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "email", "telephone", "updated_at")
    search_fields = ("prenom", "nom", "email", "telephone")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CreneauCalendrier)
class CreneauCalendrierAdmin(admin.ModelAdmin):
    list_display = ("date", "heure_debut", "heure_fin", "statut", "motif_reserve", "urgence", "client")
    list_filter = ("statut", "urgence", "date", "motif_reserve")
    search_fields = ("client__email", "client__nom", "motif_reserve__nom")
    actions = ("create_standard_two_weeks", "mark_blocked", "mark_free")

    @admin.action(description="Créer les créneaux libres standards sur 2 semaines")
    def create_standard_two_weeks(self, _request, _queryset):
        today = date.today()
        for day_offset in range(14):
            current = today + timedelta(days=day_offset)
            if current.weekday() >= 5:
                continue
            for start, end in [(time(9, 0), time(12, 30)), (time(14, 0), time(18, 0))]:
                CreneauCalendrier.objects.get_or_create(date=current, heure_debut=start, heure_fin=end)

    @admin.action(description="Bloquer les créneaux sélectionnés")
    def mark_blocked(self, _request, queryset):
        queryset.update(statut=CreneauCalendrier.Statut.BLOQUE)

    @admin.action(description="Libérer les créneaux sélectionnés")
    def mark_free(self, _request, queryset):
        queryset.update(statut=CreneauCalendrier.Statut.LIBRE, motif_reserve=None, client=None)


@admin.register(Rdv)
class RdvAdmin(admin.ModelAdmin):
    list_display = ("contact", "motif", "urgence", "statut", "created_at")
    list_filter = ("motif", "urgence", "statut", "created_at")
    search_fields = ("contact__email", "contact__nom", "contact__prenom")
    readonly_fields = ("notification_status", "created_at", "updated_at")


@admin.register(RdvRappel)
class RdvRappelAdmin(admin.ModelAdmin):
    list_display = ("rdv", "type_rappel", "scheduled_at", "status", "sent_at")
    list_filter = ("type_rappel", "status", "scheduled_at")
