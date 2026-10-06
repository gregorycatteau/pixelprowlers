import graphene

import audits.schema
import crm.schema
import urgencies.schema


class Query(
    audits.schema.Query,
    crm.schema.Query,
    urgencies.schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    audits.schema.Mutation,
    crm.schema.Mutation,
    urgencies.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
