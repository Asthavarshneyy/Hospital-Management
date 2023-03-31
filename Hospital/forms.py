from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'gender', 'address', 'phone_number', 'blood_group', 'medical_history']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class PharmacistForm(forms.ModelForm):
    class Meta:
        model = Pharmacist
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['aadhaar_number'].widget.attrs['readonly'] = True

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = Medical_History
        fields = ['diagnosis', 'treatment', 'file']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address']