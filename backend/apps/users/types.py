from graphene_django import DjangoObjectType
from .models import Organization

class OrganizationsType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"