# Generated by Django 3.2 on 2022-05-25 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olympiads', '0014_auto_20220524_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='finish_try_time',
        ),
        migrations.RemoveField(
            model_name='result',
            name='start_try_time',
        ),
    ]