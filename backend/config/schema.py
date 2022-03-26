import graphene
from graphene_django.debug import DjangoDebug

import users.schema
# import courses.schema
# import olympiads.schema


class Query(users.schema.Query,  graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(users.schema.Mutation,  graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)
