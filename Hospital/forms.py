from django import forms
from .models import *

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = Medical_History
        fields = '__all__'

class MedicalFileForm(forms.ModelForm):
    class Meta:
        model = Medical_File
        fields = '__all__'
        widgets = {'file': forms.ClearableFileInput(attrs={'multiple': True})}

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ('aadhaar_number', 'first_name', 'last_name', 'email', 'dob', 'age', 'sex', 'address',
                       'phone_number', 'blood_group', 'password')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        # Save the user's password securely
        user = super(PatientForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_aadhaar_number(self):
        aadhaar_number = self.cleaned_data['aadhaar_number']
        if Patient.objects.filter(aadhaar_number=aadhaar_number).exists():
            raise forms.ValidationError("A patient with this aadhaar number already exists.")
        return aadhaar_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email address already exists.")
        return email
    
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }