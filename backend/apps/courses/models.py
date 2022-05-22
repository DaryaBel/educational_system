from django.db import models

from organizations.models import Organization
from users.models import Student, Subject


STUDYING_FORM = [
    ('ON', 'Онлайн'),
    ('OFF', 'Оффлайн'),
    ('BOTH', 'Смешанный'),
]

DURATION_CHOICES = [
    ('LESSMONTH', 'Меньше месяца'),
    ('MONTH', '1-2 месяца'),
    ('FEWMONTH', 'От двух месяцев до полугода'),
    ('HALFYEAR', 'От полугода до года'),
    ('YEARANDMORE', 'Год и более'),
]

# Города
class City(models.Model):
    name = models.CharField("Название", max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

# Курсы
class Course(models.Model):
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    duration = models.CharField(verbose_name="Длительность", max_length=20, choices=DURATION_CHOICES, null=True, blank=True)
    form = models.CharField(verbose_name="Формат проведения", max_length=20, choices=STUDYING_FORM)
    date_start = models.DateField("Дата начала", null=True, blank=True)
    date_end = models.DateField("Дата окончания", null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация", related_name="organizationCourse")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город проведения", null=True, blank=True, related_name="cityCourse")
    max_number_member = models.PositiveIntegerField("Максимальное количество слушателей", null=True, blank=True)
    published = models.BooleanField("Опубликовано", default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        

# Школьники на курсах
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Школьник", related_name="studentCourse")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="courseStudent")
    
    def __str__(self):
        return f"{self.student}. {self.course}"

    class Meta:
        verbose_name = "Школьник, записанный на курс"
        verbose_name_plural = "Школьники, записанные на курсы"

# Предметы курса
class CourseSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, verbose_name="Предмет", related_name="subjectCourse", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="courseSubject")
    
    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Предмет курса"
        verbose_name_plural = "Предметы курсов"





