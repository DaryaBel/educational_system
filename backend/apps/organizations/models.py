from django.db import models

ORGANIZATION_KIND_CHOICES = [
    ('UNIVERSITY', 'Высшее учебное заведение'),
    ('COMPANY', 'Компания'),
]

# Организации
class Organization(models.Model):
    fullname = models.CharField("Полное название", max_length=150)
    shortname = models.CharField("Краткое название", max_length=150, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    kind = models.CharField(verbose_name="Вид организации", max_length=12, choices=ORGANIZATION_KIND_CHOICES)
    logo = models.ImageField("Логотип", upload_to='logo', null=True, blank=True)
    
    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

