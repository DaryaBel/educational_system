from django.db import models

from users.models import User, City, Student, Subject

STUDYING_FORM = [
    ('ON', 'Онлайн'),
    ('OFF', 'Оффлайн'),
    ('BOTH', 'Смешанная'),
]

DURATION_TYPE = [
    ('LESSMONTH', 'Меньше месяца'),
    ('MONTH', '1-2 месяца'),
    ('FEWMONTH', 'От двух месяцев до полугода'),
    ('HALFYEAR', 'От полугода до года'),
    ('YEARANDMORE', 'Год и более'),
]

# Вузы
class University(models.Model):
    fullname = models.CharField("Полное название", max_length=150)
    shortname = models.CharField("Краткое название", max_length=150, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name="cityUniversity")
    logo = models.ImageField("Логотип", upload_to='logo', null=True, blank=True)
    
    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Вуз"
        verbose_name_plural = "Вузы"

# Cотрудники вуза
class UniversityStaff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="userUniversityStaff")
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="Вуз", related_name="universityUniversityStaff")
    position = models.CharField("Должность", max_length=150, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Cотрудник вуза"
        verbose_name_plural = "Cотрудники вуза"


# Курсы
class Course(models.Model):
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    duration = models.CharField(verbose_name="Длительность", max_length=20, choices=DURATION_TYPE)
    form = models.CharField(verbose_name="Формат проведения", max_length=20, choices=STUDYING_FORM)
    date_start = models.DateField("Дата начала", null=True, blank=True)
    date_end = models.DateField("Дата окончания", null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.CASCADE, verbose_name="Вуз", related_name="universityCourse")
    max_number_member = models.PositiveIntegerField("Максимальное количество слушателей", null=True, blank=True)
    is_draft = models.BooleanField("Черновик", default=False)
    
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





