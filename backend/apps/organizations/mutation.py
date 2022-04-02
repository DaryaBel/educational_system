import graphene
from organizations.models import City, Organization, OrganizationCity
from organizations.types import CityType, OrganizationCityType, OrganizationType

class CreateOrganization(graphene.Mutation):
    class Arguments:
        fullname = graphene.String(required=True)
        shortname = graphene.String()
        kind = graphene.String(required=True)
        description = graphene.String()
        # logo = graphene.String()
        
    ok = graphene.Boolean()
    organization = graphene.Field(OrganizationType)

    @classmethod
    def mutate(cls, root, info, fullname, kind, description=None, shortname=None):
        organization = Organization.objects.create(
            fullname=fullname, shortname=shortname, description=description, kind=kind)

        return cls(ok=True, organization=organization)

class CreateCity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        
    ok = graphene.Boolean()
    city = graphene.Field(CityType)

    @classmethod
    def mutate(cls, root, info, name):
        city = City.objects.create(
            name=name)

        return cls(ok=True, city=city)

class CreateOrganizationCity(graphene.Mutation):
    class Arguments:
        city_id = graphene.ID(required=True)
        organization_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()
    organizationCity = graphene.Field(OrganizationCityType)

    @classmethod
    def mutate(cls, root, info, city_id, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        city = City.objects.get(pk=city_id)
        organizationCity = OrganizationCity.objects.create(
            city=city, organization=organization)

        return cls(ok=True, organizationCity=organizationCity)

class DeleteOrganization(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        organization.delete()

        return cls(ok=True)

class DeleteCity(graphene.Mutation):
    class Arguments:
        city_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, city_id):
        city = City.objects.get(pk=city_id)
        city.delete()

        return cls(ok=True)

class DeleteOrganizationCity(graphene.Mutation):
    class Arguments:
        organization_city_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, organization_city_id):
        organization_city = OrganizationCity.objects.get(pk=organization_city_id)
        organization_city.delete()

        return cls(ok=True)

class UpdateOrganization(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)
        fullname = graphene.String()
        shortname = graphene.String()
        kind = graphene.String()
        description = graphene.String()
        # logo = graphene.String()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, organization_id, fullname=None, description=None, shortname=None, kind=None):
        organization = Organization.objects.get(pk=organization_id)
        if fullname != None:
            organization.fullname = fullname
        if shortname != None:
            organization.shortname = shortname
        if description != None:
            organization.description = description
        if kind != None:
            organization.kind = kind    
        organization.save()

        return cls(ok=True)

class UpdateCity(graphene.Mutation):
    class Arguments:
        city_id = graphene.ID(required=True)
        name = graphene.String()
        
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, city_id, name):
        city = City.objects.get(pk=city_id)
        city.name = name
        city.save()

        return cls(ok=True)