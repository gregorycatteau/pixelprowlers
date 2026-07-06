import graphene
from graphene_django import DjangoObjectType

from audits.models import (
    AuditDossier,
    AuditReponse,
    RefonteAudit,
    Citation,
    Motif,
    RaisonAppel,
    RdvContact,
    CreneauCalendrier,
    Rdv,
    RdvRappel,
)


class AuditDossierType(DjangoObjectType):
    class Meta:
        model = AuditDossier
        fields = "__all__"


class AuditReponseType(DjangoObjectType):
    class Meta:
        model = AuditReponse
        fields = "__all__"


class RefonteAuditType(DjangoObjectType):
    class Meta:
        model = RefonteAudit
        fields = "__all__"


class CitationType(DjangoObjectType):
    class Meta:
        model = Citation
        fields = "__all__"


class MotifType(DjangoObjectType):
    class Meta:
        model = Motif
        fields = "__all__"


class RaisonAppelType(DjangoObjectType):
    class Meta:
        model = RaisonAppel
        fields = "__all__"


class RdvContactType(DjangoObjectType):
    class Meta:
        model = RdvContact
        fields = "__all__"


class CreneauCalendrierType(DjangoObjectType):
    class Meta:
        model = CreneauCalendrier
        fields = "__all__"


class RdvType(DjangoObjectType):
    class Meta:
        model = Rdv
        fields = "__all__"


class RdvRappelType(DjangoObjectType):
    class Meta:
        model = RdvRappel
        fields = "__all__"
