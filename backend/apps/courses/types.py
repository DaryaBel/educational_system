from courses.models import Course, CourseSubject, StudentCourse
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
    class Meta:
        model = CourseSubject
        fields = "__all__"