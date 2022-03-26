from django.contrib import admin

from courses.models import Course, CourseSubject, StudentCourse

class StudentCourseInline(admin.StackedInline):
    model = StudentCourse
    extra = 0

class CourseSubjectInline(admin.StackedInline):
    model = CourseSubject
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    """Курсы"""
    list_display = ('__str__', 'organization', 'form', 'published',)
    list_filter = ('form', 'duration')
    search_fields = ('name', 'organization', 'description',)
    inlines = [CourseSubjectInline, StudentCourseInline]
    
admin.site.register(Course, CourseAdmin)