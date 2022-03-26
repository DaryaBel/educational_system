from django.db import models

ORGANIZATION_TYPE = [
    ('UNIVERSITY', 'Высшее учебное заведение'),
    ('COMPANY', 'Компания'),
]

# Города
class City(models.Model):
    name = models.CharField("Название", max_length=150)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

# Организации
class Organization(models.Model):
    fullname = models.CharField("Полное название", max_length=150)
    shortname = models.CharField("Краткое название", max_length=150, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    type = models.CharField(verbose_name="Вид организации", max_length=12, choices=ORGANIZATION_TYPE)
    logo = models.ImageField("Логотип", upload_to='logo', null=True, blank=True)
    
    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

# Города организации
class OrganizationCity(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация", related_name="organizationCity")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name="cityOrganization")
    
    def __str__(self):
        return f"{self.organization}. {self.city}"

    class Meta:
        verbose_name = "Город организации"
        verbose_name_plural = "Города организаций"
        
