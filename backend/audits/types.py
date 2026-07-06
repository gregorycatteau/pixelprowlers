import graphene
from graphene_django import DjangoObjectType

from .models import (
    AuditDossier,
    AuditReponse,
    Citation,
    CreneauCalendrier,
    Motif,
    RaisonAppel,
    Rdv,
    RdvContact,
    RefonteAudit,
)


class AuditDossierType(DjangoObjectType):
    class Meta:
        model = AuditDossier
        fields = [
            "id",
            "numero_dossier",
            "prenom",
            "nom",
            "email",
            "telephone",
            "type_personne",
            "nom_structure",
            "consentement_rgpd",
            "date_creation",
            "statut",
            "notification_status",
        ]


class AuditReponseType(DjangoObjectType):
    score_global = graphene.String()

    class Meta:
        model = AuditReponse
        fields = [
            "id",
            "dossier",
            "reponses",
            "scores_series",
            "pilier_faible",
            "date_soumission",
        ]

    def resolve_score_global(self, info):
        return str(self.score_global)


class RefonteAuditType(DjangoObjectType):
    class Meta:
        model = RefonteAudit
        fields = [
            "id",
            "reference",
            "prenom",
            "nom",
            "email",
            "telephone",
            "type_personne",
            "nom_structure",
            "site_url",
            "reponses",
            "analysis_status",
            "technical_report",
            "pagespeed_report",
            "heuristic_report",
            "analysis_error",
            "date_creation",
            "date_maj",
        ]


class CitationType(DjangoObjectType):
    class Meta:
        model = Citation
        fields = [
            "id",
            "numero",
            "texte",
            "auteur",
            "source",
            "langue",
            "theme",
            "annee",
            "actif",
            "verifie",
            "nb_affichages",
        ]


class MotifType(DjangoObjectType):
    class Meta:
        model = Motif
        fields = ["id", "nom", "duree_minutes", "creneau_type", "actif", "ordre"]


class RaisonAppelType(DjangoObjectType):
    class Meta:
        model = RaisonAppel
        fields = ["id", "nom", "actif", "ordre"]


class RdvContactType(DjangoObjectType):
    class Meta:
        model = RdvContact
        fields = ["id", "prenom", "nom", "email", "telephone", "audit_dossier"]


class CreneauCalendrierType(DjangoObjectType):
    class Meta:
        model = CreneauCalendrier
        fields = ["id", "date", "heure_debut", "heure_fin", "statut", "motif_reserve", "urgence"]


class RdvType(DjangoObjectType):
    class Meta:
        model = Rdv
        fields = [
            "id",
            "contact",
            "motif",
            "creneaux",
            "raisons",
            "urgence",
            "message",
            "statut",
            "notification_status",
            "created_at",
        ]


# Types "utilitaires" pour les résolveurs qui renvoient des dicts (pas des modèles)

class CreneauDisponibleType(graphene.ObjectType):
    date = graphene.String()
    heure_debut = graphene.String()
    heure_fin = graphene.String()


class JourCalendrierType(graphene.ObjectType):
    date = graphene.String()
    statut = graphene.String()
    disponible = graphene.Boolean()
