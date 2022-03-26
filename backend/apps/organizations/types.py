from graphene_django import DjangoObjectType
from organizations.models import City, Organization, OrganizationCity

class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"

class CityType(DjangoObjectType):
    class Meta:
        model = City
        fields = "__all__"

class OrganizationCityType(DjangoObjectType):
    class Meta:
        model = OrganizationCity
        fields = "__all__"