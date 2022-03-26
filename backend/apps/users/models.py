from uuid import uuid4

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from organizations.models import Organization, City

class UserManager(BaseUserManager):
    def _create_user(
            self,
            email,
            password,
            is_staff,
            is_superuser,
            **extra_fields):
        """
        Создаёт и сохраняет Пользователя с данными логином, email и паролем.
        """
        user = self.model(email=self.normalize_email(email),
                          is_active=True,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          last_login=timezone.now(),
                          registered_at=timezone.now(),
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        is_staff = extra_fields.pop('is_staff', False)
        is_superuser = extra_fields.pop('is_superuser', False)
        return self._create_user(
            email,
            password,
            is_staff,
            is_superuser,
            **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=255)
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
        default='Имя')
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
        default='Фамилия')
    # avatar = models.ImageField(verbose_name='Avatar', blank=True)
    token = models.UUIDField(
        verbose_name='Токен',
        default=uuid4,
        editable=False)

    is_admin = models.BooleanField(verbose_name='Администратор', default=False)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_staff = models.BooleanField(verbose_name='Сотрудник', default=False)
    registered_at = models.DateTimeField(
        verbose_name='Зарегистрирован',
        auto_now_add=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    full_name.fget.short_description = 'Имя и фамилия'

    @property
    def short_name(self):
        return f'{self.last_name} {self.first_name[0]}.'
    short_name.fget.short_description = 'Имя'

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.full_name


# Cотрудники
class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="userEmployee")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация", related_name="organizationEmployee")
    position = models.CharField("Должность", max_length=150, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Cотрудник"
        verbose_name_plural = "Cотрудники"

# Школьники
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="userStudent")
    patronymic = models.CharField("Отчество", max_length=150, null=True, blank=True)
    birthdate = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name="cityStudent")
    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Школьник"
        verbose_name_plural = "Школьники"

# Предметы
class Subject(models.Model):
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

# Предметы школьников
class StudentSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет", related_name="subjectStudent")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Школьник", related_name="studentSubject")
    
    def __str__(self):
        return f"{self.subject}. {self.student}"

    class Meta:
        verbose_name = "Предмет школьника"
        verbose_name_plural = "Предметы школьников"