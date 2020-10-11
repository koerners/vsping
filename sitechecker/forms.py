from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
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
        fields = ['name', 'url', 'check_every', 'check_until']
