import graphene
from graphene_django.debug import DjangoDebug

import users.schema
import organizations.schema
import courses.schema
import olympiads.schema


class Query(users.schema.Query, organizations.schema.Query, courses.schema.Query, olympiads.schema.Query, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


class Mutation(users.schema.Mutation, organizations.schema.Mutation, courses.schema.Mutation,  graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutation)

