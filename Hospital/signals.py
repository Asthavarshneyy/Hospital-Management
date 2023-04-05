from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

def create_user(instance):
    user = User.objects.create_user(
        username=instance.aadhaar_number,
        password=instance.aadhaar_number,
        email=instance.email,
        first_name=instance.first_name,
        last_name=instance.last_name
    )
    instance.user = user
    instance.save()

@receiver(post_save, sender=Patient)
def create_patient_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_save, sender=Doctor)
def create_doctor_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_save, sender=Nurse)
def create_doctor_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_save, sender=Receptionist)
def create_doctor_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_save, sender=Pharmacist)
def create_doctor_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_save, sender=Administrator)
def create_doctor_user(sender, instance, created, **kwargs):
    if created:
        create_user(instance)

@receiver(post_delete, sender=Patient)
def delete_patient_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Doctor)
def delete_staff_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Nurse)
def delete_staff_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Receptionist)
def delete_staff_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Administrator)
def delete_staff_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()

@receiver(post_delete, sender=Pharmacist)
def delete_staff_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()