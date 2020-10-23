from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from sitechecker.models import Job


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'url', 'check_every', 'threshold']
        labels = {
            'threshold': 'Alert Threshold in %',
        }


class UpdateJobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['name', 'url', 'check_every', 'threshold', 'is_active']

        widgets = {
            'threshold': forms.NumberInput(attrs={'min': 0, 'max': 100})
        }
        labels = {
            'threshold': 'Alert Threshold in %'
        }
