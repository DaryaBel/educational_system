import graphene
from courses.models import Course
from courses.types import CourseType
from organizations.models import Organization

class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    published_courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, course_id=graphene.ID(required=True))
    courses_organization = graphene.List(CourseType, organization_id=graphene.ID(required=True))
    published_courses_organization = graphene.List(CourseType, organization_id=graphene.ID(required=True))

    def resolve_courses(root, info):
        return Course.objects.all()

    def resolve_published_courses(root, info):
        return Course.objects.filter(published=True)

    def resolve_course(root, info, course_id):
        return Course.objects.get(pk=course_id)

    def resolve_courses_organization(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization)

    def resolve_published_courses_organization(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization, published=True)

schema = graphene.Schema(query=Query)    