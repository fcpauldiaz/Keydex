from __future__ import unicode_literals

from django.forms import ModelForm, PasswordInput, CharField, TextInput, Form
from main.models import User
from registration.forms import RegistrationForm

class SignUpForm(ModelForm):
  first_name = CharField(widget=TextInput())
  last_name = CharField(widget=TextInput())
  class Meta:
    model = User
    fields = ['username', 'password', 'email', 'first_name', 'last_name']

class LoginForm(ModelForm):
  password = CharField(widget=PasswordInput)
  class Meta:
    model = User
    fields = ['username','password']

class ResetPasswordForm(ModelForm):
  username = CharField(widget=TextInput())
# class ForgotForm(ModelForm)
  class Meta:
    model = User
    fields = ['username']

class ChangePasswordForm(Form):
  password = CharField(widget=PasswordInput)
  password_repeated = CharField(widget=PasswordInput)

