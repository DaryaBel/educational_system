# Generated by Django 3.2 on 2022-03-22 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_employee_organization_organizationcity'),
        ('olympiads', '0004_auto_20220202_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycity',
            name='city',
        ),
        migrations.RemoveField(
            model_name='companycity',
            name='company',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='company',
        ),
        migrations.RemoveField(
            model_name='employer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='olympiad',
            name='company',
        ),
        migrations.AddField(
            model_name='olympiad',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='organizationOlympiad', to='users.organization', verbose_name='Организация'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='CompanyCity',
        ),
        migrations.DeleteModel(
            name='Employer',
        ),
    ]