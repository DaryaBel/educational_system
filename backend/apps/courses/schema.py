from courses.mutation import CreateCity, CreateCourse, CreateCourseSubject, CreateStudentCourse, DeleteCity, DeleteCourse,  DeleteCourseSubject, DeleteStudentCourse, UpdateCity, UpdateCourse
import graphene
from courses.models import City, Course, StudentCourse
from courses.types import CityType, CourseType, StudentCourseType
from organizations.models import Organization
from users.models import Student, User

class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    published_courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, course_id=graphene.ID(required=True))
    organization_courses = graphene.List(CourseType, organization_id=graphene.ID(required=True))
    published_courses_organization = graphene.List(CourseType, organization_id=graphene.ID(required=True))
    student_courses = graphene.List(CourseType, user_id=graphene.ID(required=True))
    course_students = graphene.List(StudentCourseType, course_id=graphene.ID(required=True))
    count_course_member = graphene.Int(course_id=graphene.ID(required=True))
    is_student_course_member = graphene.Boolean(course_id=graphene.ID(required=True), user_id=graphene.ID(required=True))
    cities = graphene.List(CityType)
    city = graphene.Field(CityType, city_id=graphene.ID(required=True))

    def resolve_courses(root, info):
        return Course.objects.all()

    def resolve_published_courses(root, info):
        return Course.objects.filter(published=True)

    def resolve_course(root, info, course_id):
        return Course.objects.get(pk=course_id)

    def resolve_organization_courses(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization)

    def resolve_published_courses_organization(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization, published=True)

    def resolve_student_courses(root, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            student = Student.objects.get(user=user)
            studentCourse = StudentCourse.objects.filter(student=student)
            courses = []
            for studentCourse in studentCourse:
                courses += [studentCourse.course]
            return courses
        except Exception as e:
            return None  

    def resolve_course_students(root, info, course_id):
        course = Course.objects.get(pk=course_id)
        return StudentCourse.objects.filter(course=course)

    def resolve_count_course_member(root, info, course_id):
        course = Course.objects.get(pk=course_id)
        return StudentCourse.objects.filter(course=course).count()

    def resolve_is_student_course_member(root, info, course_id, user_id):
        course = Course.objects.get(pk=course_id)
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        return StudentCourse.objects.filter(course=course, student=student)

    def resolve_cities(root, info):
        return City.objects.all()

    def resolve_city(root, info, city_id):
        return City.objects.get(pk=city_id)

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_student_course = CreateStudentCourse.Field()
    create_course_subject = CreateCourseSubject.Field()
    delete_course = DeleteCourse.Field()
    delete_student_course = DeleteStudentCourse.Field()
    delete_course_subject = DeleteCourseSubject.Field()
    update_course = UpdateCourse.Field()
    create_city = CreateCity.Field()
    delete_city = DeleteCity.Field()
    update_city = UpdateCity.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)    