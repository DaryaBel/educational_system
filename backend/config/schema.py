import graphene
from graphene_django.debug import DjangoDebug

import users.schema


class Query(users.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(users.schema.Mutation, graphene.ObjectType):
    ...


schema = graphene.Schema(query=Query, mutation=Mutation)
