from unittest import result
import graphene
from olympiads.models import Olympiad, Result
from olympiads.types import OlympiadType, ResultType
from users.models import Student, User

class Query(graphene.ObjectType):
    olympiads = graphene.List(OlympiadType)
    olympiad = graphene.Field(OlympiadType, olympiad_id=graphene.ID(required=True))
    published_olympiads = graphene.List(OlympiadType)
    student_olympiads = graphene.List(OlympiadType, user_id=graphene.ID(required=True))
    student_olympiad_result = graphene.Field(ResultType, user_id=graphene.ID(required=True), olympiad_id=graphene.ID(required=True))
    
    def resolve_olympiads(root, info):
        return Olympiad.objects.all()

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

    def resolve_student_olympiad_result(root, info, olympiad_id, user_id):
        try:
            olympiad = Olympiad.objects.get(pk=olympiad_id)
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            return Result.objects.get(olympiad=olympiad, student=student)
        except Exception as e:
            return None

schema = graphene.Schema(query=Query)    