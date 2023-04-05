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
    list_display = ('aadhaar_number', 'get_name', 'email', 'speciality', 'department', 'job_title')
    list_filter = ('department', 'blood_group','is_active', 'is_employed',)
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



