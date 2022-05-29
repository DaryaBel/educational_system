import graphene
from olympiads.models import Answer, Olympiad, OlympiadSubject, Result, Task
from olympiads.types import AnswerType, OlympiadSubjectType, OlympiadType, ResultType, TaskType
from organizations.models import Organization
from users.models import Student, Subject, User

class CreateOlympiad(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        percent_to_win = graphene.Int(required=True)
        organization_id = graphene.ID(required=True)
        date_result = graphene.Date()
        date_end = graphene.Date()
        
    ok = graphene.Boolean()
    olympiad = graphene.Field(OlympiadType)

    @classmethod
    def mutate(cls, root, info, name, percent_to_win, organization_id, description=None, date_result=None, date_end=None):
        organization = Organization.objects.get(pk=organization_id)
        olympiad = Olympiad.objects.create(
            name=name, published=False, percent_to_win=percent_to_win, organization=organization, description=description, date_result=date_result, date_end=date_end)

        return cls(ok=True, olympiad=olympiad)

class CreateTask(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)
        task = graphene.String(required=True)
        max_score = graphene.Int(required=True)
        order = graphene.Int(required=True)
        
    ok = graphene.Boolean()
    task = graphene.Field(TaskType)

    @classmethod
    def mutate(cls, root, info, olympiad_id, task, max_score, order):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        task = Task.objects.create(
            olympiad=olympiad, task=task, max_score=max_score, order=order)

        return cls(ok=True, task=task)

class CreateResult(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        score = graphene.Int()
        
    ok = graphene.Boolean()
    result = graphene.Field(ResultType)

    @classmethod
    def mutate(cls, root, info, olympiad_id, user_id, score=None):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        
        result = Result.objects.create(
            olympiad=olympiad, published=False, status="TAKEPART", won=False, student=student, score=score)

        return cls(ok=True, result=result)

class CreateAnswer(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        olympiad_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)
        answer = graphene.String(required=True)
        score = graphene.Int()
        
    ok = graphene.Boolean()
    answer = graphene.Field(AnswerType)

    @classmethod
    def mutate(cls, root, info, task_id, olympiad_id, user_id, answer, score=None):
        task = Task.objects.get(pk=task_id)
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        result = Result.objects.get(student=student, olympiad=olympiad)
        answer = Answer.objects.create(
            result=result, task=task, answer=answer, score=score)

        return cls(ok=True, answer=answer)

class CreateOlympiadSubject(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)
        subject_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()
    olympiadSubject = graphene.Field(OlympiadSubjectType)

    @classmethod
    def mutate(cls, root, info, olympiad_id, subject_id):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        subject = Subject.objects.get(pk=subject_id)
        olympiadSubject = OlympiadSubject.objects.create(
            subject=subject, olympiad=olympiad)

        return cls(ok=True, olympiadSubject=olympiadSubject)
        
class DeleteOlympiad(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, olympiad_id):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        olympiad.delete()

        return cls(ok=True)

class DeleteTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, task_id):
        task = Task.objects.get(pk=task_id)
        task.delete()

        return cls(ok=True)

class DeleteResult(graphene.Mutation):
    class Arguments:
        result_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, result_id):
        result = Result.objects.get(pk=result_id)
        result.delete()

        return cls(ok=True)

class DeleteAnswer(graphene.Mutation):
    class Arguments:
        answer_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, answer_id):
        answer = Answer.objects.get(pk=answer_id)
        answer.delete()

        return cls(ok=True)


class DeleteOlympiadSubject(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)
        subject_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, olympiad_id, subject_id):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        subject = Subject.objects.get(pk=subject_id)
        olympiadSubject = OlympiadSubject.objects.get(
            subject=subject, olympiad=olympiad)
        olympiadSubject.delete()

        return cls(ok=True)

class UpdateOlympiad(graphene.Mutation):
    class Arguments:
        olympiad_id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        percent_to_win = graphene.Int()
        date_result = graphene.Date()
        date_end = graphene.Date()
        published = graphene.Boolean()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, olympiad_id, published=None, name=None, percent_to_win=None, description=None, date_result=None, date_end=None):
        olympiad = Olympiad.objects.get(pk=olympiad_id)
        if name != None:
            olympiad.name = name
        if description != None:
            olympiad.description = description
        if percent_to_win != None:
            olympiad.percent_to_win = percent_to_win
        if date_result != None:
            olympiad.date_result = date_result
        if date_end != None:
            olympiad.date_end = date_end
        if published != None:
            olympiad.published = published
        olympiad.save()
    
        return cls(ok=True)

class UpdateTask(graphene.Mutation):
    class Arguments:
        task_id = graphene.ID(required=True)
        task = graphene.String()
        max_score = graphene.Int()
        order = graphene.Int()
        
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, task_id, task=None, max_score=None, order=None):
        one_task = Task.objects.get(pk=task_id)
        if task != None:
            one_task.task = task
        if max_score != None:
            one_task.max_score = max_score
        if order != None:
            one_task.order = order
        one_task.save()
    
        return cls(ok=True)

class UpdateResult(graphene.Mutation):
    class Arguments:
        result_id = graphene.ID(required=True)
        score = graphene.Int()
        status = graphene.String()
        won = graphene.Boolean()
        published = graphene.Boolean()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, result_id, score=None, status=None, won=None, published=None):
        result = Result.objects.get(pk=result_id)
        if score != None:
            result.score = score
        if status != None:
            result.status = status
        if won != None:
            result.won = won
        if published != None:
            result.published = published
        result.save()

        return cls(ok=True)

class UpdateAnswer(graphene.Mutation):
    class Arguments:
        answer_id = graphene.ID(required=True)
        answer = graphene.String()
        score = graphene.Int()
        
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, answer_id, answer=None, score=None):
        one_answer = Answer.objects.get(pk=answer_id)
        if answer != None:
            one_answer.answer = answer
        if score != None:
            one_answer.score = score
        one_answer.save()

        return cls(ok=True)