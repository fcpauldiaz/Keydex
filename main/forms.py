from __future__ import unicode_literals

from django.forms import ModelForm, PasswordInput, CharField
from main.models import User

class SignUpForm(ModelForm):
  password = CharField(widget=PasswordInput)
  class Meta:
    model = User
    fields = ['first_name', 'last_name', 'username','email', 'password']

