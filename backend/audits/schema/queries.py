import random

import graphene
from django.db.models import F, Max, Min
from graphql import GraphQLError

from audits.models import (
    Citation,
    Motif,
    RaisonAppel,
    RefonteAudit,
    AuditDossier,
)
from audits.rdv_services import available_slots, calendar_month

from .types import (
    CitationType,
    MotifType,
    RaisonAppelType,
    RefonteAuditType,
    AuditDossierType,
)


class CreneauDisponibleType(graphene.ObjectType):
    date = graphene.String()
    heure_debut = graphene.String()
    heure_fin = graphene.String()


class JourCalendrierType(graphene.ObjectType):
    date = graphene.String()
    statut = graphene.String()


class Query(graphene.ObjectType):
    citation_aleatoire = graphene.Field(CitationType, exclude_id=graphene.Int())

    motifs = graphene.List(MotifType)
    raisons_appel = graphene.List(RaisonAppelType)

    refonte_audit = graphene.Field(RefonteAuditType, reference=graphene.String(required=True))
    audit_dossier = graphene.Field(AuditDossierType, numero_dossier=graphene.String(required=True))

    creneaux_disponibles = graphene.List(
        CreneauDisponibleType,
        motif_id=graphene.Int(required=True),
        date_debut=graphene.Date(required=True),
        date_fin=graphene.Date(required=True),
        urgence=graphene.Boolean(default_value=False),
    )

    calendrier_mois = graphene.List(
        JourCalendrierType,
        annee=graphene.Int(required=True),
        mois=graphene.Int(required=True),
    )

    def resolve_citation_aleatoire(root, info, exclude_id=None):
        queryset = Citation.objects.filter(actif=True, numero__isnull=False)

        if exclude_id and queryset.count() > 1:
            queryset = queryset.exclude(id=exclude_id)

        bounds = queryset.aggregate(min_numero=Min("numero"), max_numero=Max("numero"))
        min_numero = bounds["min_numero"]
        max_numero = bounds["max_numero"]

        if min_numero is None or max_numero is None:
            raise GraphQLError("Aucune citation active disponible.")

        target = random.randint(min_numero, max_numero)
        citation = queryset.filter(numero__gte=target).order_by("numero").first()

        if not citation:
            citation = queryset.order_by("numero").first()

        if citation:
            Citation.objects.filter(pk=citation.pk).update(nb_affichages=F("nb_affichages") + 1)
            citation.refresh_from_db(fields=["nb_affichages"])

        return citation

    def resolve_motifs(root, info):
        return Motif.objects.filter(actif=True)

    def resolve_raisons_appel(root, info):
        return RaisonAppel.objects.filter(actif=True)

    def resolve_refonte_audit(root, info, reference):
        try:
            return RefonteAudit.objects.get(reference=reference)
        except RefonteAudit.DoesNotExist:
            raise GraphQLError("Audit refonte introuvable.")

    def resolve_audit_dossier(root, info, numero_dossier):
        try:
            return AuditDossier.objects.get(numero_dossier=numero_dossier)
        except AuditDossier.DoesNotExist:
            raise GraphQLError("Dossier introuvable.")

    def resolve_creneaux_disponibles(root, info, motif_id, date_debut, date_fin, urgence=False):
        try:
            motif = Motif.objects.get(id=motif_id, actif=True)
        except Motif.DoesNotExist as exc:
            raise GraphQLError("Motif indisponible.") from exc

        if date_fin < date_debut:
            raise GraphQLError("La date de fin doit être postérieure à la date de début.")

        results = available_slots(motif, date_debut, date_fin, urgence)

        return [
            CreneauDisponibleType(
                date=r["date"],
                heure_debut=r["heure_debut"],
                heure_fin=r["heure_fin"],
            )
            for r in results
        ]

    def resolve_calendrier_mois(root, info, annee, mois):
        if mois < 1 or mois > 12:
            raise GraphQLError("Le mois doit être compris entre 1 et 12.")

        results = calendar_month(annee, mois)

        return [
            JourCalendrierType(date=r["date"], statut=r["statut"])
            for r in results
        ]
