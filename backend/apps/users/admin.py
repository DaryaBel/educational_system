from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Employee, StudentSubject, User, Student, Subject
from users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['full_name', 'email']
    fieldsets = [
        ['Данные авторизации', {'fields': ['email', 'password']}],
        ['Личная информация', {'fields': ['last_name', 'first_name']}],
        ['Настройки', {'fields': ['is_staff', ]}],
        ['Важные отметки времени', {'fields': ['last_login', 'registered_at']}],
    ]
    add_fieldsets = [[None, {'classes': ['wide'], 'fields': [
        'email', 'first_name', 'last_name', 'password1', 'password2']}], ]
    search_fields = ['email', 'first_name', 'last_name',]
    ordering = ['email']
    list_filter = ['is_staff']
    readonly_fields = ['last_login', 'registered_at']


class StudentSubjectInline(admin.StackedInline):
    model = StudentSubject
    extra = 0
    
class EmployeeAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('__str__', 'organization', 'moderated',)
    search_fields = ('user', 'organization', 'position',)
    list_filter = ('moderated',)
    actions = ["moderate"]
    
    def moderate(self, request, queryset):
        # Подтвердить аккаунт
        row_update = queryset.update(moderated=True)
        message_bit = f"Количество пользователей, аккаунты которых были успешно подтверждены: {row_update}"
        self.message_user(request, f"{message_bit}")

    moderate.short_description = "Подтвердить аккаунт"
    moderate.allowed_permissions = ('change', )

class StudentAdmin(admin.ModelAdmin):
    """Школьники"""
    list_display = ('__str__', 'birthdate',)
    search_fields = ('user', 'patronymic',)
    inlines = [StudentSubjectInline]

class SubjectAdmin(admin.ModelAdmin):
    """Предметы"""
    list_display = ('__str__',)
    search_fields = ('name',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
