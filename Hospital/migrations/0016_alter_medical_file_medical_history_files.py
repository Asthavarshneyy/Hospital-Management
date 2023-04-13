# Generated by Django 4.1.7 on 2023-04-05 10:48

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0015_alter_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medical_file',
            name='medical_history_files',
            field=models.ForeignKey(blank=True, default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medical_history_files', to='Hospital.medical_history'),
        ),
    ]