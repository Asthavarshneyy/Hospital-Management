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
    class Meta:
        model = Patient
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        medical_history = Medical_History.objects.create()
        cleaned_data['medical_history'] = medical_history
        return cleaned_data