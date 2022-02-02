from django.contrib import admin

from olympiads.models import Answer, Company, Olympiad, Result, Task

class CompanyAdmin(admin.ModelAdmin):
    """Компании"""
    list_display = ('__str__',)
    search_fields = ('name', 'description',)
    
class OlympiadAdmin(admin.ModelAdmin):
    """Олимпиады"""
    list_display = ('__str__', 'company', 'is_draft',)
    search_fields = ('name', 'company', 'description',)
    
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
    list_display = ('__str__', 'score', 'is_draft',)
    search_fields = ('olympiad', 'student',)
    

admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Answer, AnswerAdmin)    
admin.site.register(Company, CompanyAdmin)
admin.site.register(Olympiad, OlympiadAdmin)