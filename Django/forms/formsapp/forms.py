# myapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Prospect, CustomUser

class ProspectForm(forms.ModelForm):
    meeting_time_date = forms.DateTimeField(
        required=False, 
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Prospect
        fields = [
            'name_of_prospect', 'number_of_vehicles', 'existing_insurer',
            'decision_maker', 'decision_maker_phone', 'meeting_time_date', 'existing_rates'
        ]

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

class AddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'password','admin']
