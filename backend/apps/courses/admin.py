from django.contrib import admin

from courses.models import Course, University

class UniversityAdmin(admin.ModelAdmin):
    """Вузы"""
    list_display = ('__str__', 'city',)
    list_filter = ('city',)
    search_fields = ('fullname', 'shortname', 'description',)
    
class CourseAdmin(admin.ModelAdmin):
    """Курсы"""
    list_display = ('__str__', 'university', 'form', 'duration', 'is_draft',)
    list_filter = ('form', 'duration')
    search_fields = ('name', 'university', 'description',)
    

admin.site.register(University, UniversityAdmin)
admin.site.register(Course, CourseAdmin)