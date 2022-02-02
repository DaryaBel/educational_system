from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from courses.models import UniversityStaff
from olympiads.models import Employer

from users.models import User, City, Student, Subject
from users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # Поля, которые используются при отображении модели пользователя.
    # Они переопределяют определения в базовом UserAdmin
    # которые ссылаются на определенные поля в auth.User.list_display = ['full_name', 'email']
    list_display = ['full_name', 'email']
    fieldsets = [
        ['Данные авторизации', {'fields': ['email', 'password']}],
        ['Личная информация', {'fields': ['last_name', 'first_name']}],
        ['Настройки', {'fields': ['groups', 'is_admin', 'is_active', 'is_staff', 'is_superuser']}],
        ['Важные отметки времени', {'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets не является стандартным атрибутом ModelAdmin. UserAdmin
    # переопределяет get_fieldsets для использования этого атрибута при создании пользователя.
    add_fieldsets = [[None, {'classes': ['wide'], 'fields': [
        'email', 'first_name', 'last_name', 'password1', 'password2']}], ]
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['last_login', 'registered_at']


class CityAdmin(admin.ModelAdmin):
    """Города"""
    list_display = ('__str__',)
    search_fields = ('name',)
    
class EmployerAdmin(admin.ModelAdmin):
    """Работодатели"""
    list_display = ('__str__', 'company', 'position',)
    search_fields = ('user', 'company', 'position',)
    
class UniversityStaffAdmin(admin.ModelAdmin):
    """Cотрудники вуза"""
    list_display = ('__str__', 'university', 'position',)
    search_fields = ('user', 'university', 'position',)

class StudentAdmin(admin.ModelAdmin):
    """Школьники"""
    list_display = ('__str__', 'birthdate', 'city',)
    list_filter = ('city',)
    search_fields = ('user', 'patronymic',)

class SubjectAdmin(admin.ModelAdmin):
    """Предметы"""
    list_display = ('__str__',)
    search_fields = ('name', 'description',)

admin.site.register(City, CityAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(UniversityStaff, UniversityStaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
