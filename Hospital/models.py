from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import time, datetime, timedelta
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

SEX_CHOICES=(
    ("M","Male"),
    ("F", "Female"),
    ("I", "Intersex"),
)

SHIFT_CHOICES=(
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('N', 'Night')
)

MEDICINE_TYPES = (
        ('tab', 'Tablet'),
        ('cap', 'Capsule'),
        ('syp', 'Syrup'),
        ('inj', 'Injection'),
        ('oth', 'Other'),
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dob=models.DateField(help_text="use YYYY-MM-DD format", default=timezone.now)
    # lets make age a derived attribute
    age = models.IntegerField(default=0)
    sex=models.CharField(max_length=10, choices=SEX_CHOICES, default='')
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
        return self.first_name+" " + self.last_name


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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dob=models.DateField(help_text="use YYYY-MM-DD format", default=timezone.now)
    # lets make age a derived attribute
    age = models.IntegerField(default=0)
    sex=models.CharField(max_length=10, choices=SEX_CHOICES, default='')
    address = models.CharField(max_length=200, default='')
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message=_("Phone number must be a 10 digit number."),
    )
    phone_number = models.CharField(max_length=10, validators=[phone_regex], default='')
    blood_group=models.CharField(max_length=10, choices=BLOOD_CHOICES, default='')
    job_title = models.CharField(max_length=100, default='')
    date_joined = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_employed= models.BooleanField(default=True)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null=True)
    experience = models.CharField(max_length=200)
    start_time = models.TimeField(default=None, blank=True, null=True)
    end_time = models.TimeField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.shift == 'M':
            self.start_time = time(hour=8, minute=0)
            self.end_time = time(hour=12, minute=0)
        elif self.shift == 'A':
            self.start_time = time(hour=12, minute=0)
            self.end_time = time(hour=16, minute=0)
        elif self.shift == 'N':
            self.start_time = time(hour=16, minute=0)
            self.end_time = time(hour=20, minute=0)
        super().save(*args, **kwargs)

    @property
    def get_name(self):
     return self.first_name+" "+self.last_name
    @property
    def get_id(self):
        return self.user.id
    class Meta:
        abstract = True

class Doctor(Staff):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    
    def __str__(self):
        return self.first_name+ " "+ self.last_name+ " " + str(self.department)
    
class Receptionist(Staff):
    responsibilities = models.TextField()
    def __str__(self):
        return self.first_name+" "+self.last_name

class Nurse(Staff):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    certification = models.CharField(max_length=100)
    responsibilities = models.TextField()
    def __str__(self):
        return self.first_name+" "+self.last_name+ " " + str(self.department)

class Pharmacist(Staff):
    license_number = models.CharField(max_length=100)
    education = models.CharField(max_length=200)
    def __str__(self):
        return self.first_name+" "+self.last_name

class Administrator(Staff):
    is_superuser = models.BooleanField(default=False)
    responsibilities = models.TextField()
    def __str__(self):
        return self.first_name+" "+self.last_name

class Appointment(models.Model):
    appointment_time = models.DateTimeField(default=None)
    description=models.CharField(max_length=50, default='')
    department = models.ForeignKey('Department', on_delete=models.CASCADE, related_name='department_appointment')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_appointment')
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_appointment')
    status=models.CharField(max_length=40, choices=STATUS_CHOICES, default="Active")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_appointment')
    problem=models.TextField(max_length=200, default='')
    
    class Meta:
        unique_together = (('appointment_time', 'doctor'), ('appointment_time', 'patient'))

    def clean(self):
        super().clean()
        if self.appointment_time:
            if self.appointment_time.time() < self.doctor.start_time or \
               self.appointment_time.time() >= self.doctor.end_time:
                raise ValidationError("Appointment time must be within doctor's working hours.")

            existing_appointments = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_time__date=self.appointment_time.date(),
                status='Active'
            )

            # Will add that feature later on
            # available_slots = self.doctor.available_slots(self.appointment_time.date())
            # if self.appointment_time not in available_slots:
            #     raise ValidationError("Appointment time not available. Available timeslots: {}".format(", ".join(map(str, available_slots))))

            # conflicting_appointment = existing_appointments.filter(
            #     appointment_time=self.appointment_time
            # ).first()

            # if conflicting_appointment is not None:
            #     raise ValidationError("Appointment time conflicts with an existing appointment.")


class Inventory(models.Model):
    medicine_name = models.CharField(max_length=255, default='')
    medicine_type = models.CharField(max_length=3, choices=MEDICINE_TYPES)
    description = models.TextField(default='')
    manufacturer = models.CharField(max_length=255, default='')
    supplier = models.CharField(max_length=255, default='')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=0)
    medicine_use = models.TextField(default='')
    minimum_quantity = models.PositiveIntegerField(default=0, help_text="Minimum quantity before restocking is required")
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manufacturing_date=models.DateField(help_text="use YYYY-MM-DD format", default=timezone.now)
    isbn_number=models.BigIntegerField(unique=True, default=0)
    is_available=models.BooleanField(default=False)
    expiry_date = models.DateField()
    def __str__(self):
        return f"{self.medicine_name} ({self.medicine_type})"
    
    @property
    def isAvailable(self):
        return self.quantity >= self.minimum_quantity
    
    def save(self, *args, **kwargs):
        self.is_available = self.isAvailable
        super(Inventory, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ['-updated_at']

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
    medical_history_files = models.ForeignKey('Medical_History', on_delete=models.CASCADE, related_name='medical_history_files', default=None, null=True, blank=True)
    def __str__(self):
        return self.name
    
class Medical_History(models.Model):
    files = models.ManyToManyField('Medical_File', related_name='files', null=True, blank=True)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, related_name='patient_medical_history', default=None, null=True, blank=True)
    def __str__(self):
        return self.patient.aadhaar_number
    

