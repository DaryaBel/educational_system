# Generated by Django 3.2 on 2022-03-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_rename_is_draft_course_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]
