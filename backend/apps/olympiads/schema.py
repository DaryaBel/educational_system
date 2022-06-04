from unittest import result
import graphene
from olympiads.models import Answer, Olympiad, Result, Task
from olympiads.mutation import CreateAnswer, CreateOlympiad, CreateOlympiadSubject, CreateResult, CreateTask, DeleteAnswer, DeleteOlympiad, DeleteOlympiadSubject, DeleteResult, DeleteTask, UpdateAnswer, UpdateOlympiad, UpdateResult, UpdateTask
from olympiads.types import AnswerType, OlympiadType, ResultType, TaskType
from organizations.models import Organization
from users.models import Student, User

class Query(graphene.ObjectType):
    olympiads = graphene.List(OlympiadType)
    olympiad = graphene.Field(OlympiadType, olympiad_id=graphene.ID(required=True))
    published_olympiads = graphene.List(OlympiadType)
    student_olympiads = graphene.List(OlympiadType, user_id=graphene.ID(required=True))
    result = graphene.Field(ResultType, user_id=graphene.ID(required=True), olympiad_id=graphene.ID(required=True))
    results = graphene.List(ResultType, olympiad_id=graphene.ID(required=True))
    count_not_checked_results = graphene.Int(olympiad_id=graphene.ID(required=True))
    organization_olympiads = graphene.List(OlympiadType, organization_id=graphene.ID(required=True))
    olympiad_students = graphene.List(ResultType, olympiad_id=graphene.ID(required=True))
    tasks = graphene.List(TaskType, olympiad_id=graphene.ID(required=True))
    answers = graphene.List(AnswerType, olympiad_id=graphene.ID(required=True), user_id=graphene.ID(required=True))

    def resolve_olympiads(root, info):
        try:    
            return Olympiad.objects.all()
        except Exception as e:
            return None

    def resolve_organization_olympiads(root, info, organization_id):
        try:
            organization = Organization.objects.get(pk=organization_id)
            return Olympiad.objects.filter(organization=organization)
        except Exception as e:
            return None

    def resolve_olympiad(root, info, olympiad_id):
        try:    
            return Olympiad.objects.get(pk=olympiad_id)
        except Exception as e:
            return None

    def resolve_published_olympiads(root, info):
        try:    
            return Olympiad.objects.filter(published=True)
        except Exception as e:
            return None


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
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            return Result.objects.filter(olympiad=olympiad)
        except Exception as e:
            return None

    def resolve_tasks(root, info, olympiad_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            return Task.objects.filter(olympiad=olympiad)
        except Exception as e:
            return None

    def resolve_result(root, info, olympiad_id, user_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            return Result.objects.get(olympiad=olympiad, student=student)
        except Exception as e:
            return None

    def resolve_results(root, info, olympiad_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            return Result.objects.filter(olympiad=olympiad)
        except Exception as e:
            return None
    
    def resolve_count_not_checked_results(root, info, olympiad_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            return Result.objects.filter(olympiad=olympiad).exclude(status="CHECKED").count()
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
    create_olympiad = CreateOlympiad.Field()
    create_task = CreateTask.Field()
    create_result = CreateResult.Field()
    create_answer = CreateAnswer.Field()
    create_olympiad_subject = CreateOlympiadSubject.Field()
    
    delete_olympiad = DeleteOlympiad.Field()
    delete_task = DeleteTask.Field()
    delete_result = DeleteResult.Field()
    delete_answer = DeleteAnswer.Field()
    delete_olympiad_subject = DeleteOlympiadSubject.Field()
    
    update_olympiad = UpdateOlympiad.Field()
    update_task = UpdateTask.Field()
    update_result = UpdateResult.Field()
    update_answer = UpdateAnswer.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)    