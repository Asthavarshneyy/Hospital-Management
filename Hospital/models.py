from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
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
    aadhaar_regex = RegexValidator(
        regex=r'^\d{12}$',
        message=_("Aadhaar card number must be a 12 digit number."),
    )
    aadhaar_number = models.CharField(
        _("Aadhaar Card Number"),
        max_length=12,
        validators=[aadhaar_regex],
        null=False,
        unique=True
    )
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField(help_text="use YYYY-MM-DD format", default=timezone.now)
    # lets make age a derived attribute
    age = models.IntegerField(default=0)
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='')
    address = models.CharField(max_length=200, default='')
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message=_("Phone number must be a 10 digit number."),
    )
    phone_number = models.CharField(max_length=10, validators=[phone_regex], default='')
    blood_group=models.CharField(max_length=10, choices=BLOOD_CHOICES, default='')
    @property
    def get_name(self):
     return self.first_name+" "+self.last_name
    @property
    def get_id(self):
        return self.user.id
    class Meta:
        abstract = True

class Patient(Person):
   medical_history=models.OneToOneField('Medical_History', on_delete=models.CASCADE, related_name='medical_history_patient', default=None, null=True, blank=True)
   def __str__(self):
        return self.first_name+self.last_name

# not sure about it
class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Staff(models.Model):
    aadhaar_regex = RegexValidator(
        regex=r'^\d{12}$',
        message=_("Aadhaar card number must be a 12 digit number."),
    )
    aadhaar_number = models.CharField(
        _("Aadhaar Card Number"),
        max_length=12,
        validators=[aadhaar_regex],
        null=False,
        unique=True
    )
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob=models.DateField(help_text="use YYYY-MM-DD format", default=timezone.now)
    # lets make age a derived attribute
    age = models.IntegerField(default=0)
    gender=models.CharField(max_length=10, choices=GENDER_CHOICES, default='')
    address = models.CharField(max_length=200, default=0)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message=_("Phone number must be a 10 digit number."),
    )
    phone_number = models.CharField(max_length=10, validators=[phone_regex], default='')
    blood_group=models.CharField(max_length=10, choices=BLOOD_CHOICES, default='')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100, default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_employed= models.BooleanField(default=True)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null=True)
    experience = models.CharField(max_length=200)
    is_superuser = models.BooleanField(default=False)
    @property
    def get_name(self):
     return self.first_name+" "+self.last_name
    @property
    def get_id(self):
        return self.user.id
    class Meta:
        abstract = True

class Doctor(Staff):
    speciality = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    def __str__(self):
        return self.first_name+self.department

class Receptionist(Staff):
    responsibilities = models.TextField()

class Nurse(Staff):
    certification = models.CharField(max_length=100)
    responsibilities = models.TextField()
    def __str__(self):
        return self.first_name+self.department

class Pharmacist(Staff):
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)

class Administrator(Staff):
    responsibilities = models.TextField()

class Appointment(models.Model):
    dateOfAdmit = models.DateField(auto_now_add=True)
    dateOfDischarge=models.DateField(help_text="use DD/MM/YYYY format",default=None, blank=True, null=True)
    appointment_time = models.TimeField()
    description=models.CharField(max_length=50)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='department_appointment')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_appointment')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_appointment')
    status=models.CharField(max_length=40, choices=STATUS_CHOICES, default="Active")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_appointment')
    problem=models.TextField(max_length=200, default='')

class Inventory(models.Model):
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
    prescription=models.TextField(default=None, blank=True, null=True)
    medicine = models.ForeignKey('Inventory', on_delete=models.CASCADE, related_name='medicine_prescription')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_prescription')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_prescription')
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE, primary_key=True, related_name='appointment_prescription')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_prescription')

class Billing(models.Model):
    billing_date=models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_billing')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_billing')
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, related_name='prescriptions_billing')
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE, related_name='appointment_billing')
    def __str__(self):
        return f"Billing #{self.billing_id} for {self.patient.get_name}"

class Medical_File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='medical_files')
    date=models.DateTimeField(default=timezone.now)
    medical_history_files = models.ForeignKey('Medical_History', on_delete=models.CASCADE, related_name='medical_history_files', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Medical_History(models.Model):
    files = models.ManyToManyField('Medical_File', related_name='files', null=True, blank=True)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, related_name='patient_medical_history', default=None, null=True, blank=True)
    def __str__(self):
        return f"{self.patient.__str__}"
    

