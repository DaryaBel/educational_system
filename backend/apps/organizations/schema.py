import graphene
from organizations.models import City, Organization, OrganizationCity
from organizations.types import CityType, OrganizationType

class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)
    organization = graphene.Field(OrganizationType, organization_id=graphene.ID(required=True))
    organizations_company = graphene.List(OrganizationType)
    organizations_university = graphene.List(OrganizationType)
    organizations_city = graphene.List(OrganizationType, city_id=graphene.ID(required=True))
    organizations_city_company = graphene.List(OrganizationType, city_id=graphene.ID(required=True))
    organizations_city_university = graphene.List(OrganizationType, city_id=graphene.ID(required=True))

    cities = graphene.List(CityType)
    city = graphene.Field(CityType, city_id=graphene.ID(required=True))
    
    def resolve_organizations(root, info):
        return Organization.objects.all()

    def resolve_organization(root, info, organization_id):
        return Organization.objects.get(pk=organization_id)

    def resolve_organizations_company(root, info):
        return Organization.objects.filter(kind='COMPANY')

    def resolve_organizations_university(root, info):
        return Organization.objects.filter(kind='UNIVERSITY')  

    def resolve_organizations_city(root, info, city_id):
        try:
            organizationCity = OrganizationCity.objects.filter(city=city_id)
            organizations = []
            for organizationCity in organizationCity:
                organizations += [organizationCity.organization]
            return organizations
        except Exception as e:
            return None  

    def resolve_organizations_city_company(root, info, city_id):
        try:
            organizationCity = OrganizationCity.objects.filter(city=city_id)
            organizations = []
            for organizationCity in organizationCity:
                organizations += [organizationCity.organization]
            result = filter(lambda organization: organization.kind == 'COMPANY', organizations)
            return result
        except Exception as e:
            return None 

    def resolve_organizations_city_university(root, info, city_id):
        try:
            organizationCity = OrganizationCity.objects.filter(city=city_id)
            organizations = []
            for organizationCity in organizationCity:
                organizations += [organizationCity.organization]
            result = filter(lambda organization: organization.kind == 'UNIVERSITY', organizations)
            return result
        except Exception as e:
            return None    

    def resolve_cities(root, info):
        return City.objects.all()

    def resolve_city(root, info, city_id):
        return City.objects.get(pk=city_id)

schema = graphene.Schema(query=Query)    