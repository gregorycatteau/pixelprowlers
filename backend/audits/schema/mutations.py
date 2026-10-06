import graphene
from pixelprowlers.abuse import allow, client_ip, require_quota
from graphql import GraphQLError

from audits.models import AuditDossier
from pixelprowlers.object_access import grant_object, owned_object, require_same_origin
from audits.rdv_services import reserve_rdv
from audits.serializers import (
    AuditDossierCreateSerializer,
    AuditSubmitSerializer,
    RefonteAuditCreateSerializer,
    RdvReservationSerializer,
)
from .types import AuditDossierType, RefonteAuditType, RdvType


def _serializer_errors_to_message(errors) -> str:
    parts = []
    for field, messages in errors.items():
        if isinstance(messages, (list, tuple)):
            joined = " ".join(str(message) for message in messages)
        else:
            joined = str(messages)
        parts.append(f"{field}: {joined}")
    return " | ".join(parts) if parts else "Erreur de validation."


def _request_from_info(info):
    context = getattr(info, "context", None)
    return getattr(context, "request", context)


def _client_ip(request):
    address = client_ip(request)
    return None if address == "unknown" else address


def _check_rate_limit(request, action: str, limit: int) -> bool:
    return allow(request, "audit:" + action, limit, 15 * 60)


class CreateAuditDossier(graphene.Mutation):
    class Arguments:
        prenom = graphene.String(required=True)
        nom = graphene.String(required=True)
        email = graphene.String(required=True)
        telephone = graphene.String(required=True)
        type_personne = graphene.String(required=True)
        nom_structure = graphene.String(required=False)
        consentement_rgpd = graphene.Boolean(required=True)

    dossier = graphene.Field(AuditDossierType)

    def mutate(self, info, **kwargs):
        request = _request_from_info(info)
        if not _check_rate_limit(request, "create", 8):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        require_same_origin(request)
        serializer = AuditDossierCreateSerializer(data=kwargs)
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))
        dossier = serializer.save()
        grant_object(request, "audit", dossier.numero_dossier, dossier.pk)
        return CreateAuditDossier(dossier=dossier)


class SubmitAuditReponses(graphene.Mutation):
    class Arguments:
        numero_dossier = graphene.String(required=True)
        reponses = graphene.JSONString(required=True)

    numero_dossier = graphene.String()
    statut = graphene.String()
    scores_series = graphene.JSONString()
    score_global = graphene.String()
    pilier_faible = graphene.String()
    notification_status = graphene.JSONString()

    def mutate(self, info, numero_dossier, reponses):
        if not isinstance(reponses, dict):
            raise GraphQLError("Le champ reponses doit être un objet JSON.")

        request = _request_from_info(info)
        if not _check_rate_limit(request, "submit", 12):
            raise GraphQLError("Trop de soumissions en peu de temps. Réessayez dans quelques minutes.")

        authorized = owned_object(request, "audit", numero_dossier, AuditDossier)
        serializer = AuditSubmitSerializer(
            data={
                "numero_dossier": numero_dossier,
                "reponses": reponses,
            },
            context={
                "authorized_dossier": authorized,
                "ip_address": _client_ip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT", "") if request is not None else "",
            },
        )
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        reponse = serializer.save()
        dossier = reponse.dossier
        return SubmitAuditReponses(
            numero_dossier=dossier.numero_dossier,
            statut=dossier.statut,
            scores_series=reponse.scores_series,
            score_global=str(reponse.score_global),
            pilier_faible=reponse.pilier_faible,
            notification_status=dossier.notification_status,
        )


class CreateRefonteAudit(graphene.Mutation):
    class Arguments:
        prenom = graphene.String(required=True)
        nom = graphene.String(required=True)
        email = graphene.String(required=True)
        telephone = graphene.String(required=True)
        type_personne = graphene.String(required=True)
        nom_structure = graphene.String(required=False)
        site_url = graphene.String(required=True)
        consentement_rgpd = graphene.Boolean(required=True)
        reponses = graphene.JSONString(required=True)

    audit = graphene.Field(RefonteAuditType)

    def mutate(self, info, **kwargs):
        reponses = kwargs.get("reponses")
        if not isinstance(reponses, dict):
            raise GraphQLError("Le champ reponses doit être un objet JSON.")

        request = _request_from_info(info)
        if not _check_rate_limit(request, "refonte-create", 6):
            raise GraphQLError("Trop de demandes en peu de temps. Réessayez dans quelques minutes.")

        require_same_origin(request)
        serializer = RefonteAuditCreateSerializer(data=kwargs)
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))
        audit = serializer.save()
        grant_object(request, "refonte", audit.reference, audit.pk)
        return CreateRefonteAudit(audit=audit)


class CreateRdvReservation(graphene.Mutation):
    class Arguments:
        motif_id = graphene.Int(required=True)
        date = graphene.Date(required=True)
        heure_debut = graphene.String(required=True)
        heure_fin = graphene.String(required=True)
        urgence = graphene.Boolean(required=False, default_value=False)
        prenom = graphene.String(required=True)
        nom = graphene.String(required=True)
        email = graphene.String(required=True)
        telephone = graphene.String(required=True)
        raison_ids = graphene.List(graphene.Int, required=True)
        message = graphene.String(required=False)

    rdv = graphene.Field(RdvType)

    def mutate(self, info, **kwargs):
        require_quota(_request_from_info(info), "reservation-create", 5, 900)
        serializer = RdvReservationSerializer(data=kwargs)
        if not serializer.is_valid():
            raise GraphQLError(_serializer_errors_to_message(serializer.errors))

        try:
            rdv = serializer.save()
        except ValueError as exc:
            raise GraphQLError(str(exc)) from exc

        return CreateRdvReservation(rdv=rdv)


class Mutation(graphene.ObjectType):
    create_audit_dossier = CreateAuditDossier.Field()
    submit_audit_reponses = SubmitAuditReponses.Field()
    create_refonte_audit = CreateRefonteAudit.Field()
    create_rdv_reservation = CreateRdvReservation.Field()
