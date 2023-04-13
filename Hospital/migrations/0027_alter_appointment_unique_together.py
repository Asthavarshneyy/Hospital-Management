# Generated by Django 4.1.7 on 2023-04-05 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0026_alter_appointment_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('appointment_time', 'doctor'), ('appointment_time', 'patient')},
        ),
    ]