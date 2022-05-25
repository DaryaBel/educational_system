import graphene
from organizations.models import Organization
from organizations.mutation import CreateOrganization, DeleteOrganization, UpdateOrganization
from organizations.types import OrganizationType

class Query(graphene.ObjectType):
    organizations = graphene.List(OrganizationType)
    organization = graphene.Field(OrganizationType, organization_id=graphene.ID(required=True))
    organizations_company = graphene.List(OrganizationType)
    organizations_university = graphene.List(OrganizationType)
    
    def resolve_organizations(root, info):
        try:
            return Organization.objects.all()
        except Exception as e:
            return None

    def resolve_organization(root, info, organization_id):
        try:
            return Organization.objects.get(pk=organization_id)
        except Exception as e:
            return None

    def resolve_organizations_company(root, info):
        try:
            return Organization.objects.filter(kind='COMPANY')
        except Exception as e:
            return None

    def resolve_organizations_university(root, info):
        try:
            return Organization.objects.filter(kind='UNIVERSITY')  
        except Exception as e:
            return None
   

class Mutation(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    update_organization = UpdateOrganization.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)    