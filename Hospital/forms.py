from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'medical_history', 'problem', 'doctor', 'appointment']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'problem': forms.Textarea(attrs={'rows': 3})
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience']

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['staff', 'amount', 'date_received', 'is_paid']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'speciality', 'license_number', 'education']

class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'responsibilities']

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'certification', 'responsibilities']

class PharmacistForm(forms.ModelForm):
    class Meta:
        model = Pharmacist
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'license_number', 'education']

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = ['first_name', 'last_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'responsibilities']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['dateOfAdmit', 'dateOfDischarge', 'appointment_time', 'description', 'doctor', 'patient', 'status']

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['medicine_name', 'price', 'quantity', 'medicine_use', 'manufacturing_date', 'isbn_number', 'isAvailable', 'expiry_date']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['appointment', 'medicine', 'patient', 'doctor', 'prescription']

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['billing_date', 'total_amount', 'payment_mode', 'patient', 'doctor', 'staff_responsible', 'prescription', 'appointment']
