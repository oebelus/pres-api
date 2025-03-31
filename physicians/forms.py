from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Physician

class PhysicianRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    specialty = forms.CharField(required=True)
    hospital = forms.CharField(required=True)
    university = forms.CharField(required=True)

    class Meta:
        model = Physician
        fields = ('email', 'first_name', 'last_name', 'phone', 
                 'specialty', 'hospital', 'university', 'password1', 'password2')

class PhysicianProfileForm(forms.ModelForm):
    class Meta:
        model = Physician
        fields = ('first_name', 'last_name', 'email', 'phone', 
                 'specialty', 'hospital', 'university')

class PhysicianLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )