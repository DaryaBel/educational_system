from unittest import result
import graphene
from olympiads.models import Answer, Olympiad, Result, Task
from olympiads.types import AnswerType, OlympiadType, ResultType, TaskType
from organizations.models import Organization
from users.models import Student, User

class Query(graphene.ObjectType):
    olympiads = graphene.List(OlympiadType)
    olympiad = graphene.Field(OlympiadType, olympiad_id=graphene.ID(required=True))
    published_olympiads = graphene.List(OlympiadType)
    student_olympiads = graphene.List(OlympiadType, user_id=graphene.ID(required=True))
    student_olympiad_result = graphene.Field(ResultType, user_id=graphene.ID(required=True), olympiad_id=graphene.ID(required=True))
    organization_olympiads = graphene.List(OlympiadType, organization_id=graphene.ID(required=True))
    olympiad_students = graphene.List(ResultType, olympiad_id=graphene.ID(required=True))
    tasks = graphene.List(TaskType, olympiad_id=graphene.ID(required=True))
    answers = graphene.List(AnswerType, olympiad_id=graphene.ID(required=True), user_id=graphene.ID(required=True))

    def resolve_olympiads(root, info):
        return Olympiad.objects.all()

    def resolve_organization_olympiads(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Olympiad.objects.filter(organization=organization)

    def resolve_olympiad(root, info, olympiad_id):
        return Olympiad.objects.get(pk=olympiad_id)

    def resolve_published_olympiads(root, info):
        return Olympiad.objects.filter(published=True)

    def resolve_student_olympiads(root, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            results = Result.objects.filter(student=student)
            olympiads = []
            for result in results:
                olympiads += [result.olympiad]
            return olympiads
        except Exception as e:
            return None  

    def resolve_course_students(root, info, olympiad_id):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        return Result.objects.filter(olympiad=olympiad)

    def resolve_tasks(root, info, olympiad_id):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        return Task.objects.filter(olympiad=olympiad)

    def resolve_student_olympiad_result(root, info, olympiad_id, user_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            return Result.objects.get(olympiad=olympiad, student=student)
        except Exception as e:
            return None

    def resolve_answers(root, info, olympiad_id, user_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            result = Result.objects.get(olympiad=olympiad, student=student)
            return Answer.objects.filter(result=result)        
        except Exception as e:
            return None

class Mutation(graphene.ObjectType):
    create_olympiad = CreateCourse.Field()
    create_task = CreateStudentCourse.Field()
    create_result = CreateCourseSubject.Field()
    create_answer = CreateCourseSubject.Field()
    create_olympiad_subject = CreateCourseSubject.Field()
    
    delete_olympiad = DeleteCourse.Field()
    delete_task = DeleteStudentCourse.Field()
    delete_result = DeleteCourseSubject.Field()
    delete_answer = DeleteStudentCourse.Field()
    delete_olympiad_subject = DeleteCourseSubject.Field()
    
    update_olympiad = UpdateCourse.Field()
    update_task = UpdateCity.Field()
    update_result = UpdateCity.Field()
    update_answer = UpdateCity.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)    