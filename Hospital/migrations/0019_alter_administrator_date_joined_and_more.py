# Generated by Django 4.1.7 on 2023-04-05 13:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0018_remove_administrator_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='pharmacist',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='receptionist',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]