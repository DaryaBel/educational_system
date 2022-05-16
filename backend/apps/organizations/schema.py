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
        return Organization.objects.all()

    def resolve_organization(root, info, organization_id):
        return Organization.objects.get(pk=organization_id)

    def resolve_organizations_company(root, info):
        return Organization.objects.filter(kind='COMPANY')

    def resolve_organizations_university(root, info):
        return Organization.objects.filter(kind='UNIVERSITY')  
   

class Mutation(graphene.ObjectType):
    create_organization = CreateOrganization.Field()
    delete_organization = DeleteOrganization.Field()
    update_organization = UpdateOrganization.Field()
    
schema = graphene.Schema(query=Query, mutation=Mutation)    