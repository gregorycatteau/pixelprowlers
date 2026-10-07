from graphene_django import DjangoObjectType
import graphene
from audits.models import AuditDossier, RefonteAudit, Citation, Motif, RaisonAppel, CreneauCalendrier, Rdv

class AuditDossierType(DjangoObjectType):
    class Meta:
        model = AuditDossier
        fields = ("numero_dossier", "statut")

class RefonteAuditType(DjangoObjectType):
    followup_path = graphene.String()

    def resolve_followup_path(self, info):
        from crm.operator_services import followup_path
        return followup_path(self)

    class Meta:
        model = RefonteAudit
        fields = ("reference", "site_url", "analysis_status", "technical_report", "pagespeed_report", "heuristic_report", "analysis_error", "date_creation", "date_maj")

class CitationType(DjangoObjectType):
    class Meta:
        model = Citation
        fields = ("id", "texte", "auteur", "source")

class MotifType(DjangoObjectType):
    class Meta:
        model = Motif
        fields = ("id", "nom", "duree_minutes", "creneau_type")

class RaisonAppelType(DjangoObjectType):
    class Meta:
        model = RaisonAppel
        fields = ("id", "nom")

class CreneauCalendrierType(DjangoObjectType):
    class Meta:
        model = CreneauCalendrier
        fields = ("date", "heure_debut", "heure_fin", "statut")

class RdvType(DjangoObjectType):
    followup_path = graphene.String()

    def resolve_followup_path(self, info):
        from crm.operator_services import followup_path
        return followup_path(self)

    class Meta:
        model = Rdv
        fields = ("id", "motif", "creneaux", "statut")
