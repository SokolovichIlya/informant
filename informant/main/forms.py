from django import forms
from django.forms import ModelForm
from .models import Students, Teachers

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StudentsForm(ModelForm):
    class Meta:
        model = Students
        fields = '__all__'

class TeachersForm(ModelForm):
    class Meta:
        model = Teachers
        fields = '__all__'
