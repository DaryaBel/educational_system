import graphene
from organizations.models import Organization
from organizations.types import OrganizationType

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


class DeleteOrganization(graphene.Mutation):
    class Arguments:
        organization_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        organization.delete()

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

