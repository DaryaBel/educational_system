from django.db import models

from users.models import User, Student, Subject, City

# Компании
class Company(models.Model):
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    logo = models.ImageField("Логотип", upload_to='logo', null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

# Работодатели
class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="userEmployer")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания", related_name="companyEmployer")
    position = models.CharField("Должность", max_length=150, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатели"


# Олимпиады
class Olympiad(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания", related_name="companyOlympiad")
    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    percent_to_win = models.PositiveIntegerField("Необходимое количество % для победы")   
    time_to_pass = models.DurationField(null=True, blank=True, verbose_name='Ограничение времени для решения')
    date_result = models.DateField("Дата оглашения результатов", null=True, blank=True)
    date_end = models.DateField("Дата окончания приема ответов", null=True, blank=True)
    is_draft = models.BooleanField("Черновик", default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"

# Задания
class Task(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name="Олимпиада", related_name="olympiadTask")
    task = models.TextField("Текст задания")
    max_score = models.PositiveIntegerField("Максимальное количество баллов")   
    order = models.IntegerField(verbose_name="Номер задания", default=0, unique=True)
    
    def __str__(self):
        return f"Задание {self.order}. {self.olympiad}"

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

# Ответы
class Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задание", related_name="taskAnswer")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Школьник", related_name="studentAnswer")
    answer = models.TextField("Ответ на задание")
    score = models.PositiveIntegerField("Выставленное количество баллов", null=True, blank=True)   
    
    def __str__(self):
        return f"{self.student}. {self.task}"

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

# Результаты
class Result(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name="Олимпиада", related_name="olympiadResult")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Школьник", related_name="studentResult")
    score = models.PositiveIntegerField("Балл", null=True, blank=True)   
    certificate = models.FileField(verbose_name="Сертификат", upload_to='certificates/', null=True, blank=True)
    is_draft = models.BooleanField("Черновик", default=False)    

    def __str__(self):
        return f"{self.student}. {self.olympiad}"

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

# Города компании
class CompanyCity(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания", related_name="companyCity")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name="cityCompany")
    
    def __str__(self):
        return f"{self.company}. {self.city}"

    class Meta:
        verbose_name = "Город компании"
        verbose_name_plural = "Города компаний"

# Предметы олимпиад
class StudentSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, verbose_name="Предмет", related_name="subjectOlympiad", null=True)
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name="Олимпиада", related_name="olympiadSubject")
    
    def __str__(self):
        return f"{self.subject}. {self.olympiad}"

    class Meta:
        verbose_name = "Предмет олимпиады"
        verbose_name_plural = "Предметы олимпиад"