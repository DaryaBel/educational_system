from graphene_django import DjangoObjectType
from olympiads.models import Answer, Olympiad, OlympiadSubject, Result, Task

class OlympiadType(DjangoObjectType):
    class Meta:
        model = Olympiad
        fields = "__all__"

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"

class ResultType(DjangoObjectType):
    class Meta:
        model = Result
        fields = "__all__"

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = "__all__"

class OlympiadSubjectType(DjangoObjectType):
    class Meta:
        model = OlympiadSubject
        fields = "__all__"

