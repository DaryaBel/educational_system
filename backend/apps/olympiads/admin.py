from django.contrib import admin

from olympiads.models import Answer, Olympiad, OlympiadSubject, Result, Task

# class OlympiadSubjectInline(admin.StackedInline):
#     model = OlympiadSubject
#     extra = 0

class OlympiadAdmin(admin.ModelAdmin):
    """Олимпиады"""
    list_display = ('__str__', 'organization', 'published',)
    search_fields = ('name', 'organization', 'description',)
    # inlines = [OlympiadSubjectInline]
    
class TaskAdmin(admin.ModelAdmin):
    """Задания"""
    list_display = ('__str__',)
    search_fields = ('olympiad', 'task', '__str__',)
    
class AnswerAdmin(admin.ModelAdmin):
    """Ответы"""
    list_display = ('__str__',)
    search_fields = ('answer', '__str__', 'student', 'task',)
    
class ResultAdmin(admin.ModelAdmin):
    """Результаты"""
    list_display = ('__str__', 'status', 'published',)
    list_filter = ('status', 'published')
    search_fields = ('olympiad', 'student',)
    

admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Olympiad, OlympiadAdmin)