import graphene
import graphql_jwt

from users.models import Employee, Student, Subject, User
from users.mutation import CreateEmployee, CreateStudent, CreateStudentSubject, CreateSubject, DeleteEmployee, DeleteStudent, DeleteStudentSubject, DeleteSubject, Logout, Register, ResetPassword, ResetPasswordConfirm
from users.types import EmployeeType, StudentType, SubjectType, UserType

class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)
    profile = graphene.Field(UserType)

    employees = graphene.List(EmployeeType)
    employee = graphene.Field(EmployeeType, employee_id=graphene.ID(required=True))
    
    students = graphene.List(StudentType)
    student = graphene.Field(StudentType, student_id=graphene.ID(required=True))
    
    subjects = graphene.List(SubjectType)
    subject = graphene.Field(SubjectType, subject_id=graphene.ID(required=True))

    @staticmethod
    def resolve_user(cls, info, **kwargs):
        return User.objects.get(id=kwargs.get('id'))

    @staticmethod
    def resolve_users(cls, info, **kwargs):
        return User.objects.all()

    @staticmethod
    def resolve_profile(cls, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user

    def resolve_employees(root, info):
        return Employee.objects.all()

    def resolve_employee(root, info, employee_id):
        return Employee.objects.get(pk=employee_id)

    def resolve_students(root, info):
        return Student.objects.all()

    def resolve_student(root, info, student_id):
        return Student.objects.get(pk=student_id)

    def resolve_subjects(root, info):
        return Subject.objects.all()

    def resolve_subject(root, info, subject_id):
        return Subject.objects.get(pk=subject_id)

class Mutation(object):
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    register = Register.Field()
    logout = Logout.Field()
    reset_password = ResetPassword.Field()
    reset_password_confirm = ResetPasswordConfirm.Field()
    create_employee = CreateEmployee.Field()
    create_student = CreateStudent.Field()
    create_subject = CreateSubject.Field()
    create_student_subject = CreateStudentSubject.Field()
    delete_employee = DeleteEmployee.Field()
    delete_student = DeleteStudent.Field()
    delete_subject = DeleteSubject.Field()
    delete_student_subject = DeleteStudentSubject.Field()
    update_employee = DeleteEmployee.Field()
    update_student = DeleteStudent.Field()
    update_subject = DeleteSubject.Field()
