from django.contrib import admin

from courses.models import City, Course, CourseCity, CourseSubject, StudentCourse

class StudentCourseInline(admin.StackedInline):
    model = StudentCourse
    extra = 0

class CityAdmin(admin.ModelAdmin):
    """Города"""
    list_display = ('__str__',)
    search_fields = ('name',)

class CourseSubjectInline(admin.StackedInline):
    model = CourseSubject
    extra = 0

class CourseCityInline(admin.StackedInline):
    model = CourseCity
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    """Курсы"""
    list_display = ('__str__', 'organization', 'form', 'published',)
    list_filter = ('form', 'duration')
    search_fields = ('name', 'organization', 'description',)
    inlines = [CourseCityInline, CourseSubjectInline, StudentCourseInline]

admin.site.register(City, CityAdmin)
admin.site.register(Course, CourseAdmin)