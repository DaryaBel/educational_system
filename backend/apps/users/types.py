from graphene_django import DjangoObjectType
from users.models import Employee, Student, StudentSubject, Subject, User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'registered_at',
        ]

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