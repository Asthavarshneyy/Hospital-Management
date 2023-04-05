from django.contrib import admin
from .models import *

class MedicalHistoryInline(admin.StackedInline):
    model = Medical_History

class PatientAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'get_name', 'email', 'age', 'gender', 'address', 'phone_number', 'blood_group')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'phone_number')
    # readonly_fields = ('aadhaar_number',)
    inlines = [MedicalHistoryInline]

    def save_model(self, request, obj, form, change):
        # Create a new Medical_History instance and assign it to the new Patient instance
        obj.medical_history = Medical_History.objects.create()
        obj.medical_history.patient=obj
        super().save_model(request, obj, form, change)


admin.site.register(Patient, PatientAdmin)
admin.site.register(Medical_History)

class MedicalFileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'file', 'date',)
    search_fields = ('name', 'date',)

admin.site.register(Medical_File, MedicalFileAdmin)