from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from courses.models import City, Course, CourseSubject, StudentCourse

# class StudentCourseInline(admin.StackedInline):
#     model = StudentCourse
#     extra = 0

# class CityResource(resources.ModelResource): 
#     class Meta:
#         model = City

# class CityAdmin(ImportExportModelAdmin):
#      """Города"""
#      list_display = ('__str__',)
#      search_fields = ('name',)
#      resource_class = CityResource

# class CourseSubjectInline(admin.StackedInline):
#     model = CourseSubject
#     extra = 0

# class CourseAdmin(admin.ModelAdmin):
#     """Курсы"""
#     list_display = ('__str__', 'organization', 'form', 'published',)
#     list_filter = ('form', 'duration')
#     search_fields = ('name', 'organization', 'description',)
#     inlines = [ CourseSubjectInline, StudentCourseInline]

# admin.site.register(City, CityAdmin)
# admin.site.register(Course, CourseAdmin)