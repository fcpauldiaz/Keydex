from django.shortcuts import render, redirect
from forms import SignUpForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from models import Profile
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.template import loader
import uuid

def save_product(request):
  return render(request, 'step_2.html')