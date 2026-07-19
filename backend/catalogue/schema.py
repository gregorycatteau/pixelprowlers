import base64
import binascii

import graphene
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from .models import RefurbishedMachine


DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 50
CURSOR_PREFIX = "catalogue:"


def encode_cursor(offset):
    raw = f"{CURSOR_PREFIX}{offset}".encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def decode_cursor(cursor):
    if not cursor:
        return 0
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        decoded = base64.urlsafe_b64decode(padded.encode()).decode()
        if not decoded.startswith(CURSOR_PREFIX):
            raise ValueError
        offset = int(decoded.removeprefix(CURSOR_PREFIX)) + 1
        if offset < 0:
            raise ValueError
        return offset
    except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
        raise GraphQLError("Paramètres de pagination invalides.") from exc


class RefurbishedMachineType(graphene.ObjectType):
    slug = graphene.String(required=True)
    title = graphene.String(required=True)
    brand = graphene.String(required=True)
    model_name = graphene.String(required=True)
    summary = graphene.String(required=True)
    description = graphene.String(required=True)
    cosmetic_condition = graphene.String(required=True)
    installed_operating_system = graphene.String(required=True)
    specifications = GenericScalar(required=True)
    performed_interventions = GenericScalar(required=True)
    performed_tests = GenericScalar(required=True)
    commercial_status = graphene.String(required=True)
    price_amount = graphene.Decimal()
    currency = graphene.String(required=True)
    warranty_information = graphene.String(required=True)
    availability_note = graphene.String(required=True)
    featured = graphene.Boolean(required=True)
    seo_title = graphene.String(required=True)
    seo_description = graphene.String(required=True)
    published_at = graphene.DateTime(required=True)
    updated_at = graphene.DateTime(required=True)


class MachineEdge(graphene.ObjectType):
    cursor = graphene.String(required=True)
    node = graphene.Field(RefurbishedMachineType, required=True)


class MachinePageInfo(graphene.ObjectType):
    has_next_page = graphene.Boolean(required=True)
    end_cursor = graphene.String()


class MachineConnection(graphene.ObjectType):
    edges = graphene.List(graphene.NonNull(MachineEdge), required=True)
    page_info = graphene.Field(MachinePageInfo, required=True)


class Query(graphene.ObjectType):
    available_machines = graphene.Field(
        MachineConnection,
        first=graphene.Int(),
        after=graphene.String(),
        required=True,
    )
    refurbished_machine = graphene.Field(
        RefurbishedMachineType,
        slug=graphene.String(required=True),
    )

    def resolve_available_machines(root, info, first=DEFAULT_PAGE_SIZE, after=None):
        page_size = DEFAULT_PAGE_SIZE if first is None else first
        if page_size < 1 or page_size > MAX_PAGE_SIZE:
            raise GraphQLError(f"first doit être compris entre 1 et {MAX_PAGE_SIZE}.")
        offset = decode_cursor(after)
        queryset = RefurbishedMachine.objects.published().filter(
            commercial_status=RefurbishedMachine.CommercialStatus.AVAILABLE
        ).order_by("-featured", "display_order", "-published_at", "id")
        machines = list(queryset[offset : offset + page_size + 1])
        has_next_page = len(machines) > page_size
        machines = machines[:page_size]
        edges = [
            MachineEdge(cursor=encode_cursor(offset + index), node=machine)
            for index, machine in enumerate(machines)
        ]
        return MachineConnection(
            edges=edges,
            page_info=MachinePageInfo(
                has_next_page=has_next_page,
                end_cursor=edges[-1].cursor if edges else None,
            ),
        )

    def resolve_refurbished_machine(root, info, slug):
        return RefurbishedMachine.objects.published().exclude(
            commercial_status=RefurbishedMachine.CommercialStatus.ARCHIVED
        ).filter(slug=slug).first()
