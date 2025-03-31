from django import forms
from .models import Prescription, PrescriptionMedication
from medications.models import Medication

class MedicationSelectionForm(forms.Form):
    medication = forms.ModelChoiceField(
        queryset=Medication.objects.all(),
        widget=forms.Select(attrs={'class': 'medication-search'})
    )
    dosage_instruction = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Take 1 tablet daily'}))
    duration_days = forms.IntegerField(min_value=1, initial=7)

class PrescriptionCreateForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'notes']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'physician'):
            self.fields['patient'].queryset = user.patients.all()