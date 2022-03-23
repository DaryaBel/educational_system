from django.contrib import admin

from courses.models import Course

class CourseAdmin(admin.ModelAdmin):
    """Курсы"""
    list_display = ('__str__', 'organization', 'form', 'duration', 'is_draft',)
    list_filter = ('form', 'duration')
    search_fields = ('name', 'organization', 'description',)
    
admin.site.register(Course, CourseAdmin)