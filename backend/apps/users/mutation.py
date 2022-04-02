from turtle import position
import graphene
from uuid import uuid4
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from organizations.models import City, Organization
from users.models import Employee, Student, StudentSubject, Subject, User
from users.types import EmployeeType, StudentSubjectType, StudentType, SubjectType

class Register(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, email, password, first_name, last_name):
        if User.objects.filter(email__iexact=email).exists():
            errors = ['emailAlreadyExists']
            return Register(success=False, errors=errors)

        user = User.objects.create(
            email=email,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save()
        return Register(success=True)


class Logout(graphene.Mutation):
    success = graphene.Boolean()

    def mutate(self, info):
        logout(info.context)
        return Logout(success=True)


class ResetPassword(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            errors = ['emailDoesNotExists']
            return ResetPassword(success=False, errors=errors)

        params = {
            'user': user,
            'DOMAIN': settings.DOMAIN,
        }
        send_mail(
            subject='Password reset',
            message=render_to_string('mail/password_reset.txt', params),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return ResetPassword(success=True)


class ResetPasswordConfirm(graphene.Mutation):
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    class Arguments:
        token = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, token, password):
        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            errors = ['wrongToken']
            return ResetPasswordConfirm(success=False, errors=errors)

        user.set_password(password)
        user.token = uuid4()
        user.save()
        return ResetPasswordConfirm(success=True)

class CreateEmployee(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        organization_id = graphene.ID(required=True)
        position = graphene.String()
        
    ok = graphene.Boolean()
    employee = graphene.Field(EmployeeType)

    @classmethod
    def mutate(cls, root, info, user_id, organization_id, position=None):
        organization = Organization.objects.get(pk=organization_id)
        user = User.objects.get(pk=user_id)
        employee = Employee.objects.create(
            user=user, organization=organization, position=position)

        return cls(ok=True, employee=employee)

class CreateStudent(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        city_id = graphene.ID(required=True)
        patronymic = graphene.String()
        birthdate = graphene.Date()
        
    ok = graphene.Boolean()
    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, root, info, user_id, city_id, patronymic=None, birthdate=None):
        city = City.objects.get(pk=city_id)
        user = User.objects.get(pk=user_id)
        student = Student.objects.create(
            user=user, city=city, patronymic=patronymic, birthdate=birthdate)

        return cls(ok=True, student=student)

class CreateSubject(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        
    ok = graphene.Boolean()
    subject = graphene.Field(SubjectType)

    @classmethod
    def mutate(cls, root, info, name, description=None):
        subject = Subject.objects.create(
            name=name, description=description)

        return cls(ok=True, subject=subject)

class CreateStudentSubject(graphene.Mutation):
    class Arguments:
        student_id = graphene.ID(required=True)
        subject_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()
    studentSubject = graphene.Field(StudentSubjectType)

    @classmethod
    def mutate(cls, root, info, student_id, subject_id):
        student = Student.objects.get(pk=student_id)
        subject = Subject.objects.get(pk=subject_id)
        studentSubject = Employee.objects.create(
            student=student, subject=subject)

        return cls(ok=True, studentSubject=studentSubject)

class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()

        return cls(ok=True)

class DeleteEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, employee_id):
        employee = Employee.objects.get(pk=employee_id)
        employee.delete()

        return cls(ok=True)

class DeleteStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, student_id):
        student = Student.objects.get(pk=student_id)
        student.delete()

        return cls(ok=True)

class DeleteSubject(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, subject_id):
        subject = Subject.objects.get(pk=subject_id)
        subject.delete()

        return cls(ok=True)

class DeleteStudentSubject(graphene.Mutation):
    class Arguments:
        studentSubject_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, studentSubject_id):
        studentSubject = StudentSubject.objects.get(pk=studentSubject_id)
        studentSubject.delete()

        return cls(ok=True)

class UpdateEmployee(graphene.Mutation):
    class Arguments:
        employee_id = graphene.ID(required=True)
        position = graphene.String(required=True)
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, employee_id, position):
        employee = Employee.objects.get(pk=employee_id)
        employee.position = position  
        employee.save()

        return cls(ok=True)

class UpdateStudent(graphene.Mutation):
    class Arguments:
        student_id = graphene.ID(required=True)
        patronymic = graphene.String()
        birthdate = graphene.Date()
        city = graphene.ID()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, student_id, patronymic=None, birthdate=None, city=None):
        student = Student.objects.get(pk=student_id)
        if patronymic != None:
            student.patronymic = patronymic
        if birthdate != None:
            student.birthdate = birthdate
        if city != None:
            city = City.objects.get(pk=city)
            student.city = city
        student.save()

        return cls(ok=True)

class UpdateSubject(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, subject_id, name=None, description=None):
        subject = Student.objects.get(pk=subject_id)
        if name != None:
            subject.name = name
        if description != None:
            subject.description = description
        subject.save()

        return cls(ok=True)
