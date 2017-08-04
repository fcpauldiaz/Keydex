from __future__ import unicode_literals

import django.forms as forms
from main.models import User, ReportingPeriod
from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from validator import validate_email_unique

class SignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', validators=[validate_email_unique])
  class Meta:
      model = User
      fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )
class LoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())

class ResetPasswordForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput())
  class Meta:
    model = User
    fields = ['username']

class ChangePasswordForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput())
  password_repeated = forms.CharField(widget=forms.PasswordInput)

class AsinForm(forms.Form):
  asin = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Eg: 3801209'}))

class ProductSave(forms.Form):
  CHOICES_GROUP2=[
    ('type5','Always'),
    ('type6','Only send me an email falls below'),
  ]
  CHOICES_GROUP3=[
    ('type7', '95%'),
    ('type8', '80%'),
    ('type9', '70%'),
    ('type10', '50%')
  ]
  choices_group1 = forms.ModelChoiceField(required=False, queryset=ReportingPeriod.objects.all().order_by('value'), widget=forms.RadioSelect(attrs={'group':'group1', 'class':'with-gap', 'required': False}))
  choices_group2 = forms.ChoiceField(required=False, choices=CHOICES_GROUP2, widget=forms.RadioSelect(attrs={'group':'group2', 'class':'with-gap', 'required': False}))
  choices_group3 = forms.ChoiceField(required=False, choices=CHOICES_GROUP3, widget=forms.RadioSelect(attrs={'group':'group3', 'class':'with-gap', 'required': False}))

