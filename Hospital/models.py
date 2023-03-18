from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATUS_CHOICES=(
    ("Active", "Active"),
    ("Cancelled", "Cancelled"),
    ("Rescheduled", "Rescheduled"),
    ("Completed", "Completed"),
)

BLOOD_CHOICES=(
    ("O+","O+"),
    ("O-","O-"),
    ("A+","A+"),
    ("A-","A-"),
    ("B+","B+"),
    ("B-","B-"),
    ("AB+","AB+"),
    ("AB-","AB-"),
)

GENDER_CHOICES=(
    ("M","Male"),
    ("F", "Female"),
    ("TR", "Trans"),
    ("NB", "Non-Binary")
)

SHIFT_CHOICES=(
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('N', 'Night')
)

class Person(models.Model):
    id= models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField(help_text="use DD/MM/YYYY format")
    age = models.IntegerField()
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    blood_group=models.CharField(max_length=10, choices=BLOOD_CHOICES)
    @property
    def get_name(self):
     return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    class Meta:
        abstract = True

class Patient(Person):
    medical_history = models.TextField()
    problem=models.CharField(max_length=120)
    doctor=models.ForeignKey("Doctor", on_delete=models.CASCADE, default=None, blank=True, null=True)
    appointment_details = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name+self.last_name+" ("+self.problem+")"

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Staff(Person):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null=True)
    experience = models.CharField(max_length=200)

class Salary(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.staff) + ' - ' + str(self.amount)

class Doctor(Staff):
    speciality = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    def __str__(self):
        return self.user.first_name+self.department

class Receptionist(Staff):
    responsibilities = models.TextField()

class Nurse(Staff):
    certification = models.CharField(max_length=100)
    responsibilities = models.TextField()

class Pharmacist(Staff):
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    experience = models.CharField(max_length=200)

class Administrator(Staff):
    responsibilities = models.TextField()
    experience = models.CharField(max_length=200)

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    dateOfAdmit = models.DateField(auto_now_add=True)
    dateOfDischarge=models.DateField(help_text="use DD/MM/YYYY format",default=None, blank=True, null=True)
    appointment_time = models.TimeField()
    description=models.CharField(max_length=50)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    status=models.CharField(max_length=40, choices=STATUS_CHOICES, default="Active")

class Inventory(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=255)
    price=models.FloatField()
    quantity = models.IntegerField()
    medicine_use = models.TextField()
    manufacturing_date=models.DateField()
    isbn_number=models.BigIntegerField(default=None, blank=True, null=True)
    isAvailable=models.BooleanField(default=False)
    expiry_date = models.DateField()
    def __str__(self):
        return self.medicine_name

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, primary_key=True)
    prescription=models.TextField(default=None, blank=True, null=True)

class Billing(models.Model):
    billing_date=models.DateTimeField(auto_now_add=True)
    billing_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    staff_responsible = models.ForeignKey('Staff', on_delete=models.CASCADE)
    prescription_details = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    def __str__(self):
        return self.patient.id