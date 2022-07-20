from django import forms
from django.forms import ModelForm
from .models import Students

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = '__all__'
