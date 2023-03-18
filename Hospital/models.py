from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    id= models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)

    class Meta:
        abstract = True

class Patient(Person):
    medical_history = models.TextField()
    appointment_details = models.ForeignKey('Appointment', on_delete=models.CASCADE)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)

class Doctor(models.Model):
    speciality = models.CharField(max_length=255)
    availability = models.ForeignKey('Appointment', on_delete=models.CASCADE)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    contact = models.CharField(max_length=20)
    address = models.TextField()
    job_description = models.CharField(max_length=255)

class Receptionist(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, primary_key=True)

class Nurse(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, primary_key=True)

class Pharmacist(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, primary_key=True)

class Inventory(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    medicine_use = models.TextField()
    expiry_date = models.DateField()

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, primary_key=True)

class Billing(models.Model):
    billing_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    staff_responsible = models.ForeignKey('Staff', on_delete=models.CASCADE)
    prescription_details = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
