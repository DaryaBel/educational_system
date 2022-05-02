import graphene
from olympiads.models import Olympiad
from olympiads.types import OlympiadType

class Query(graphene.ObjectType):
    olympiads = graphene.List(OlympiadType)

    def resolve_olympiads(root, info):
        return Olympiad.objects.all()

schema = graphene.Schema(query=Query)    