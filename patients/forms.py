from django import forms
from .models import Patient
from django.contrib.auth import get_user_model

class PatientCreateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'phone', 'birthday', 'gender', 'weight']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=Patient.GENDER_CHOICES),
        }