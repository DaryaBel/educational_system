# Generated by Django 3.2 on 2022-02-02 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniversityStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=150, null=True, verbose_name='Должность')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='universityUniversityStaff', to='courses.university', verbose_name='Вуз')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userUniversityStaff', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Cотрудник вуза',
                'verbose_name_plural': 'Cотрудники вуза',
            },
        ),
    ]
