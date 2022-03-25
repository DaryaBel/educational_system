# Generated by Django 3.2 on 2022-03-25 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220325_1154'),
        ('olympiads', '0005_auto_20220322_2059'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentSubject',
            new_name='OlympiadSubject',
        ),
        migrations.AddField(
            model_name='answer',
            name='result',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resultAnswer', to='olympiads.result', verbose_name='Результат'),
            preserve_default=False,
        ),
    ]
