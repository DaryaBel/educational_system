from graphene_django import DjangoObjectType
from users.models import Employee, Student, StudentSubject, Subject

class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee
        fields = "__all__"

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = "__all__"

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject
        fields = "__all__"

class StudentSubjectType(DjangoObjectType):
    class Meta:
        model = StudentSubject
        fields = "__all__"