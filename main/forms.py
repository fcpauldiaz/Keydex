from __future__ import unicode_literals

import django.forms as forms
from main.models import User
from registration.forms import RegistrationForm

class SignUpForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'first_name', 'last_name']

class LoginForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username','password']

class ResetPasswordForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput())
  class Meta:
    model = User
    fields = ['username']

class ChangePasswordForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput)
  password_repeated = forms.CharField(widget=forms.PasswordInput)

class AsinForm(forms.Form):
  asin = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Eg: 3801209'}))
