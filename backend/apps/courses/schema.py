from courses.mutation import CreateCourse, CreateCourseSubject, CreateStudentCourse, DeleteCourse, DeleteCourseSubject, DeleteStudentCourse, UpdateCourse
import graphene
from courses.models import Course, StudentCourse
from courses.types import CourseType, StudentCourseType
from organizations.models import Organization
from users.models import Student, User

class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)
    published_courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, course_id=graphene.ID(required=True))
    courses_organization = graphene.List(CourseType, organization_id=graphene.ID(required=True))
    published_courses_organization = graphene.List(CourseType, organization_id=graphene.ID(required=True))
    student_courses = graphene.List(CourseType, student_id=graphene.ID(required=True))
    count_course_member = graphene.Int(course_id=graphene.ID(required=True))
    is_student_course_member = graphene.Boolean(course_id=graphene.ID(required=True), user_id=graphene.ID(required=True))
    
    def resolve_courses(root, info):
        return Course.objects.all()

    def resolve_published_courses(root, info):
        return Course.objects.filter(published=True)

    def resolve_course(root, info, course_id):
        return Course.objects.get(pk=course_id)

    def resolve_courses_organization(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization)

    def resolve_published_courses_organization(root, info, organization_id):
        organization = Organization.objects.get(pk=organization_id)
        return Course.objects.filter(organization=organization, published=True)

    def resolve_student_courses(root, info, student_id):
        try:
            studentCourse = StudentCourse.objects.filter(student=student_id)
            courses = []
            for studentCourse in studentCourse:
                courses += [studentCourse.course]
            return courses
        except Exception as e:
            return None  

    def resolve_count_course_member(root, info, course_id):
        course = Course.objects.get(pk=course_id)
        return StudentCourse.objects.filter(course=course).count()

    def resolve_is_student_course_member(root, info, course_id, user_id):
        course = Course.objects.get(pk=course_id)
        user = User.objects.get(pk=user_id)
        student = Student.objects.get(user=user)
        return StudentCourse.objects.filter(course=course, student=student)

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_student_course = CreateStudentCourse.Field()
    create_course_subject = CreateCourseSubject.Field()
    delete_course = DeleteCourse.Field()
    delete_student_course = DeleteStudentCourse.Field()
    delete_course_subject = DeleteCourseSubject.Field()
    update_course = UpdateCourse.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)    