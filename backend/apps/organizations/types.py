from graphene_django import DjangoObjectType
from organizations.models import Organization

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"
