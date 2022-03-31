import graphene
from courses.models import Course, CourseSubject, StudentCourse
from users.types import SubjectType
from users.models import Subject
from graphene_django import DjangoObjectType

class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = "__all__"

class StudentCourseType(DjangoObjectType):
    class Meta:
        model = StudentCourse
        fields = "__all__"

class CourseSubjectType(DjangoObjectType):
    subject = graphene.Field(SubjectType, required=True)
    class Meta:
        model = CourseSubject
        fields = "__all__"

    def resolve_subject(obj, info): 
        return Subject.objects.get(pk=obj.subject.id)