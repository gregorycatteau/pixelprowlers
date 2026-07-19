import graphene

import audits.schema
import catalogue.schema
import crm.schema
import tracking.schema
import urgencies.schema


class Query(
    audits.schema.Query,
    catalogue.schema.Query,
    crm.schema.Query,
    tracking.schema.Query,
    urgencies.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    audits.schema.Mutation,
    crm.schema.Mutation,
    tracking.schema.Mutation,
    urgencies.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
