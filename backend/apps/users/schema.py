import graphene
import graphql_jwt
from datetime import timezone, datetime
from config.settings import GRAPHQL_JWT

from users.models import Employee, Student, Subject, User
from users.mutation import CreateEmployee, CreateStudent, CreateStudentSubject, CreateSubject, DeleteEmployee, DeleteStudent, DeleteStudentSubject, DeleteSubject, Logout, Register, ResetPassword, ResetPasswordConfirm, UpdateEmployee, UpdateStudent, UpdateSubject
from users.types import EmployeeType, StudentType, SubjectType, UserType

def jwt_payload(user, context=None):
    username = user.get_username()
    student_length = Student.objects.filter(user=user).count()
    is_student = student_length > 0
    organizer_length = Employee.objects.filter(user=user).count()
    is_organizer = organizer_length > 0
    moderated = True
    if is_organizer:
        moderated = Employee.objects.filter(user=user).moderated
    return {user.USERNAME_FIELD: username, 'user_id': user.id, 'moderated': moderated, 'is_student': is_student, 'is_organizer': is_organizer, 'email': user.email, 'exp': datetime.now(timezone.utc) + GRAPHQL_JWT['JWT_EXPIRATION_DELTA']}

class Query(object):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)
    profile = graphene.Field(UserType)

    employees = graphene.List(EmployeeType)
    employee = graphene.Field(EmployeeType, user_id=graphene.ID(required=True))
    
    students = graphene.List(StudentType)
    student = graphene.Field(StudentType, user_id=graphene.ID(required=True))
    
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
        try:
            return Employee.objects.all()
        except Exception as e:
            return None

    def resolve_employee(root, info, user_id):
        try:
            user = User.objects.get(pk=user_id)          
            return Employee.objects.get(user=user)
        except Exception as e:
            return None

    def resolve_students(root, info):
        try:
            return Student.objects.all()
        except Exception as e:
            return None

    def resolve_student(root, info, user_id):
        try:
            user = User.objects.get(pk=user_id)          
            return Student.objects.get(user=user)
        except Exception as e:
            return None

    def resolve_subjects(root, info):
        try:
            return Subject.objects.all()
        except Exception as e:
            return None

    def resolve_subject(root, info, subject_id):
        try:
            return Subject.objects.get(pk=subject_id)
        except Exception as e:
            return None

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
    update_employee = UpdateEmployee.Field()
    update_student = UpdateStudent.Field()
    update_subject = UpdateSubject.Field()
