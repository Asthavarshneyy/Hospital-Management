from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

class MedicalHistoryInline(admin.StackedInline):
    model = Medical_History

class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'aadhaar_number', 'user', 'email', 'dob', 'age', 'sex', 'phone_number', 'blood_group')
    search_fields = ['aadhaar_number', 'first_name', 'last_name', 'email', 'phone_number']
    list_filter = ['blood_group',]
    ordering=('first_name',)
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
    )

    def get_name(self, obj):
        return obj.get_name
    inlines = [MedicalHistoryInline]

    def save_model(self, request, obj, form, change):
        # Create a new Medical_History instance and assign it to the new Patient instance
        obj.save()
        medical_history = Medical_History.objects.create(patient=obj)
        obj.medical_history = medical_history
        super().save_model(request, obj, form, change)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Medical_History)

class MedicalFileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'file', 'date',)
    search_fields = ('name', 'date',)

admin.site.register(Medical_File, MedicalFileAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

admin.site.register(Department,DepartmentAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'speciality', 'department', 'job_title', 'start_time', 'end_time')
    list_filter = ('department', 'blood_group','is_active', 'is_employed','start_time', 'end_time')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'speciality', 'job_title', 'education')
    ordering = ('department', 'first_name', 'date_joined')
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
        (_('Professional Information'), {
            'fields': ('department', 'job_title','date_joined', 'shift', 'speciality', 'license_number', 'education', 'experience', 'is_employed', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically sets the user to be the current user.
        """
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Doctor, DoctorAdmin)

class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'job_title')
    list_filter = ('is_active', 'is_employed','blood_group')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'job_title')
    ordering = ( 'first_name','date_joined',)
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
        (_('Professional Information'), {
            'fields': ('job_title','date_joined', 'shift', 'responsibilities', 'experience', 'is_employed', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically sets the user to be the current user.
        """
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Receptionist, ReceptionistAdmin)

class NurseAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'department', 'job_title')
    list_filter = ('is_active', 'is_employed','blood_group')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'job_title', '')
    ordering = ('department', 'first_name','date_joined')
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
        (_('Professional Information'), {
            'fields': ('department', 'job_title','date_joined', 'shift', 'experience', 'responsibilities', 'certification', 'is_employed', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically sets the user to be the current user.
        """
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Nurse, NurseAdmin)

class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'job_title')
    list_filter = ('is_active', 'is_employed','blood_group')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'job_title', 'education')
    ordering = ('first_name','date_joined')
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
        (_('Professional Information'), {
            'fields': ('job_title','date_joined', 'shift', 'license_number', 'education', 'experience', 'is_employed', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically sets the user to be the current user.
        """
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Pharmacist, PharmacistAdmin)

class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'job_title')
    list_filter = ('is_active', 'is_employed','blood_group', 'is_superuser')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email',  'job_title')
    ordering = ('first_name','date_joined')
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group',)
        }),
        (_('Professional Information'), {
            'fields': ('job_title','date_joined', 'shift', 'experience', 'responsibilities', 'is_superuser', 'is_employed', 'is_active')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Automatically sets the user to be the current user.
        """
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Administrator, AdministratorAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_time', 'department', 'doctor', 'patient', 'status')
    list_filter = ('department', 'doctor', 'status')
    search_fields = ('department__name', 'doctor__name', 'patient__name')
    date_hierarchy = 'appointment_time'
    ordering = ('appointment_time',)

admin.site.register(Appointment, AppointmentAdmin)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'medicine_type', 'description', 'manufacturer', 'supplier', 'cost_price', 'selling_price', 'quantity', 'minimum_quantity', 'is_available', 'manufacturing_date', 'isbn_number', 'expiry_date')
    list_filter = ('medicine_type', 'manufacturer', 'supplier', 'is_available', 'manufacturing_date', 'expiry_date')
    search_fields = ('medicine_name', 'description', 'manufacturer', 'supplier')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('General Information', {
            'fields': ('medicine_name', 'medicine_type', 'description', 'manufacturer', 'supplier')
        }),
        ('Price Information', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory Information', {
            'fields': ('quantity', 'minimum_quantity', 'is_available')
        }),
        ('Additional Information', {
            'fields': ('medicine_use', 'manufacturing_date', 'isbn_number', 'expiry_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Inventory, InventoryAdmin)

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date_created', 'date_modified', 'created_by', 'status')
    list_filter = ('patient', 'doctor', 'created_by', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor', 'appointment', 'created_by')
        }),
        ('Prescription Details', {
            'fields': ('prescription',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('date_created', 'date_modified')
    ordering = ['-date_modified']

admin.site.register(Prescription, PrescriptionAdmin)

class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'billing_date', 'total_amount', 'patient', 'doctor', 'prescription', 'appointment', 'status')
    list_filter = ('status', 'payment_mode', 'billing_date', 'date_created')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'appointment__appointment_date')
    fieldsets = (
        ('Billing Information', {
            'fields': ('billing_date', 'total_amount', 'status', 'payment_mode', 'billing_receipt')
        }),
        ('Related Objects', {
            'fields': ('patient', 'doctor', 'prescription', 'appointment', 'created_by')
        })
    )
    readonly_fields = ('billing_date', 'date_created', 'date_modified')
    ordering = ('-date_created',)

admin.site.register(Billing, BillingAdmin)


