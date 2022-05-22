from courses.models import City, Course, CourseSubject, StudentCourse
from courses.types import CityType,  CourseSubjectType, CourseType, StudentCourseType
import graphene
from organizations.models import Organization
from users.models import Student, Subject, User

class CreateCourse(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        duration = graphene.String()
        form = graphene.String(required=True)
        date_start = graphene.Date()
        date_end = graphene.Date()
        organization_id = graphene.ID(required=True)
        city_id = graphene.ID()
        max_number_member = graphene.Int()
        
    ok = graphene.Boolean()
    course = graphene.Field(CourseType)

    @classmethod
    def mutate(cls, root, info, name, form, organization_id, city_id=None, description=None, duration=None, date_start=None, date_end=None, max_number_member=None):
        organization = Organization.objects.get(pk=organization_id)
        city=None
        if city_id != None:
            city = City.objects.get(pk=city_id)
        course = Course.objects.create(
            name=name, form=form, organization=organization, description=description, duration=duration, published=False, date_start=date_start, date_end=date_end, max_number_member=max_number_member, city=city)

        return cls(ok=True, course=course)

class CreateCity(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        
    ok = graphene.Boolean()
    city = graphene.Field(CityType)

    @classmethod
    def mutate(cls, root, info, name):
        city = City.objects.create(
            name=name)

        return cls(ok=True, city=city)

class CreateStudentCourse(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        course_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()
    studentCourse = graphene.Field(StudentCourseType)

    @classmethod
    def mutate(cls, root, info, user_id, course_id):
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        course = Course.objects.get(pk=course_id)
        
        studentCourse = StudentCourse.objects.create(
            student=student, course=course)

        return cls(ok=True, studentCourse=studentCourse)

class CreateCourseSubject(graphene.Mutation):
    class Arguments:
        subject_id = graphene.ID(required=True)
        course_id = graphene.ID(required=True)
        
    ok = graphene.Boolean()
    courseSubject = graphene.Field(CourseSubjectType)

    @classmethod
    def mutate(cls, root, info, subject_id, course_id):
        subject = Subject.objects.get(pk=subject_id)
        course = Course.objects.get(pk=course_id)
        
        courseSubject = CourseSubject.objects.create(
            subject=subject, course=course)

        return cls(ok=True, courseSubject=courseSubject)
        
class DeleteCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, course_id):
        course = Course.objects.get(pk=course_id)
        course.delete()

        return cls(ok=True)

class DeleteCity(graphene.Mutation):
    class Arguments:
        city_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, city_id):
        city = City.objects.get(pk=city_id)
        city.delete()

        return cls(ok=True)


class DeleteStudentCourse(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        course_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, user_id, course_id):
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        course = Course.objects.get(pk=course_id)
        studentCourse = StudentCourse.objects.get(course=course, student=student)
        studentCourse.delete()

        return cls(ok=True)

class DeleteCourseSubject(graphene.Mutation):
    class Arguments:
        course_subject_id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, course_subject_id):
        courseSubject = CourseSubject.objects.get(pk=course_subject_id)
        courseSubject.delete()

        return cls(ok=True)

class UpdateCourse(graphene.Mutation):
    class Arguments:
        course_id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        duration = graphene.String()
        form = graphene.String()
        date_start = graphene.Date()
        date_end = graphene.Date()
        organization_id = graphene.ID()
        city_id = graphene.ID()
        max_number_member = graphene.Int()
        published = graphene.Boolean()
        
    ok = graphene.Boolean()
    
    @classmethod
    def mutate(cls, root, info, course_id, name=None, form=None, organization_id=None, city_id=None, published=None, description=None, duration=None, date_start=None, date_end=None, max_number_member=None):
        course = Course.objects.get(pk=course_id)
        if name != None:
            course.name = name
        if form != None:
            course.form = form
        if description != None:
            course.description = description
        if organization_id != None:
            organization = Organization.objects.get(pk=organization_id)
            course.organization = organization
        if city_id != None:
            city = City.objects.get(pk=city_id)
            course.city = city        
        if published != None:
            course.published = published
        if duration != None:
            course.duration = duration
        if date_start != None:
            course.date_start = date_start
        if date_end != None:
            course.date_end = date_end
        if max_number_member != None:
            course.max_number_member = max_number_member
        course.save()

        return cls(ok=True)

class UpdateCity(graphene.Mutation):
    class Arguments:
        city_id = graphene.ID(required=True)
        name = graphene.String()
        
    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, city_id, name):
        city = City.objects.get(pk=city_id)
        city.name = name
        city.save()

        return cls(ok=True)