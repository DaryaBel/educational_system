# Generated by Django 3.2 on 2022-03-22 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220202_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150, verbose_name='Полное название')),
                ('shortname', models.CharField(blank=True, max_length=150, null=True, verbose_name='Краткое название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('is_university', models.BooleanField(default=False, verbose_name='Высшее учебное заведение')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logo', verbose_name='Логотип')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='OrganizationCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cityOrganization', to='users.city', verbose_name='Город')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizationCity', to='users.organization', verbose_name='Организация')),
            ],
            options={
                'verbose_name': 'Город организации',
                'verbose_name_plural': 'Города организаций',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=150, null=True, verbose_name='Должность')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizationEmployee', to='users.organization', verbose_name='Организация')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userEmployee', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Cотрудник',
                'verbose_name_plural': 'Cотрудники',
            },
        ),
    ]
