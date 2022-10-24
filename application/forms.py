from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime

from django.contrib.auth.models import User
from .models import *


class AddClientForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Name')
    surname = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}), label='Surname')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control"}), label='Email')
    id_doctor = forms.CharField(widget=forms.NumberInput(attrs={'class': "form-control"}), label='Doctor ID')
    time_of_analyse = forms.DateTimeField(initial=datetime.datetime.now())
    is_corona = forms.CheckboxInput(attrs={'class': "form-control"})

    class Meta:
        model = Clients
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(label='Surname', widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': "form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))
    is_staff = forms.CheckboxInput(attrs={'value': 'Is Doctor'})

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', "password2", "is_staff")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))
