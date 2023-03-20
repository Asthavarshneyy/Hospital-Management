from django.contrib import admin
from .models import *
# Register your models here.
class PatientAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'medical_history', 'problem', 'doctor', 'appointment']
  search_fields = ['first_name', 'last_name']
admin.site.register(Patient, PatientAdmin)

class DepartmentAdmin(admin.ModelAdmin):
  list_display = ['id', 'name']
  search_fields = ['name']
admin.site.register(Department, DepartmentAdmin)

class StaffAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience']
  search_fields = ['first_name', 'last_name']
admin.site.register(Staff, StaffAdmin)

class SalaryAdmin(admin.ModelAdmin):
  list_display = ['id', 'staff', 'amount', 'date_received', 'is_paid']
  search_fields = ['staff']
admin.site.register(Salary, SalaryAdmin)

class DoctorAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'speciality', 'license_number', 'education']
  search_fields = ['first_name', 'last_name']
admin.site.register(Doctor, DoctorAdmin)

class ReceptionistAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'responsibilities']
  search_fields = ['first_name', 'last_name']
admin.site.register(Receptionist, ReceptionistAdmin)

class NurseAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'certification', 'responsibilities']
  search_fields = ['first_name', 'last_name']
admin.site.register(Nurse, NurseAdmin)

class PharmacistAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'license_number', 'education']
  search_fields = ['first_name', 'last_name']
admin.site.register(Pharmacist, PharmacistAdmin)

class AdministratorAdmin(admin.ModelAdmin):
  list_display = ['id', 'get_name', 'department', 'job_title', 'date_joined', 'is_active', 'is_superuser', 'shift', 'experience', 'responsibilities']
  search_fields = ['first_name', 'last_name']
admin.site.register(Administrator, AdministratorAdmin)

class AppointmentAdmin(admin.ModelAdmin):
  list_display = ['id', 'dateOfAdmit', 'dateOfDischarge', 'appointment_time', 'description', 'doctor', 'patient', 'status']
  search_fields = ['patient', 'doctor']
admin.site.register(Appointment, AppointmentAdmin)

class InventoryAdmin(admin.ModelAdmin):
  list_display = ['id', 'medicine_name', 'price', 'quantity', 'medicine_use', 'manufacturing_date', 'isbn_number', 'isAvailable', 'expiry_date']
  search_fields = ['medicine_name']
admin.site.register(Inventory, InventoryAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
  list_display = ['appointment', 'medicine', 'patient', 'doctor', 'prescription']
  search_fields = ['patient', 'doctor']
admin.site.register(Prescription, PrescriptionAdmin)

class BillingAdmin(admin.ModelAdmin):
  list_display = ['id', 'billing_date', 'total_amount', 'payment_mode', 'patient', 'doctor', 'staff_responsible', 'prescription', 'appointment']
  search_fields = ['patient', 'doctor']
admin.site.register(Billing, BillingAdmin)

