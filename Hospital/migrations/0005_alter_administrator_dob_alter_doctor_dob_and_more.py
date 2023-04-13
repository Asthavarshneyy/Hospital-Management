# Generated by Django 4.1.7 on 2023-04-04 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0004_alter_medical_history_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now, help_text='use YYYY-MM-DD format'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now, help_text='use YYYY-MM-DD format'),
        ),
        migrations.AlterField(
            model_name='nurse',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now, help_text='use YYYY-MM-DD format'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='dob',
            field=models.DateField(default='', help_text='use YYYY-MM-DD format'),
        ),
        migrations.AlterField(
            model_name='pharmacist',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now, help_text='use YYYY-MM-DD format'),
        ),
        migrations.AlterField(
            model_name='receptionist',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now, help_text='use YYYY-MM-DD format'),
        ),
    ]