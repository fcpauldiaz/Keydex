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


def index(request):
  return render(
    request,
    'index.html'
  )

def loginUser(request):
  if request.user.is_authenticated():
      return redirect('products_save_product')
  if request.method == 'GET':
    form = LoginForm()
    return render(
      request,
      'login.html',
      {
          'form': form
      }
    )
  elif request.method == 'POST':
    form = LoginForm(request.POST)
    user = authenticate(
      username=request.POST['username'],
      password=request.POST['password'],
    )
    if user is not None:
        login(request, user)
        return render(
          request,
          'step_2.html'
        )
    else:
      #not valid credentials
      return render(
        request,
        'login.html'
      )
  else:
    "other method"

def createUser(request):
  message = ''
  if request.messagethod == 'GET':
      user_form = SignUpForm()

  elif request.method == 'POST':
    user_form = SignUpForm(request.POST)
    message = "User created successfully"
    if user_form.is_valid():
      user = user_form.save()
      # hash password with default pdfk algorithm
      user.set_password(user.password)
      user.save()
      auth_user = authenticate(
        username=user.username,
        password=user_form.cleaned_data['password'],
      )
      login(request, auth_user)
      user_form = SignUpForm()
  else:
      pass
  return render(
      request,
      'sign_up.html',
      {
          'user_form': user_form,
          'message': message
      }
  )

def logout_view(request):
  logout(request)
  return render(
    request,
    'index.html',
  )

def reset_password(request):
  if request.method == 'GET':
    form = ResetPasswordForm()
    return render(
      request,
      'reset_password.html',
      {
          'form': form
      }
    )
  else:
    user = User.objects.get(username=request.POST['username'])
    # if user is not found
    if user == None:
      return redirect('users_reset_password') 


    # if user already has a profile attached  
    if hasattr(user, 'profile') and user.profile.password_reset_token != None: 
      dt = timezone.now() - user.profile.password_reset_token_expiration
      hours = dt.seconds/60/60
      print hours >= 1
      if hours >= 1:
        user.profile.password_reset_token = uuid.uuid4()
        user.profile.password_reset_token_expiration = timezone.now()
        user.profile.save()
        send_mail(
          'Reset password Keydex',
          'http://' + request.META['HTTP_HOST'] + '/users/token/' + str(user.profile.password_reset_token),
          'do-not-reply@keydex.com',
          [user.email],
          fail_silently=False,
        )
        return redirect('main_index')
      else:
        # wait one hour before ask for another reset password token
        return redirect('users_reset_password') 
    if hasattr(user, 'profile') and user.profile.password_reset_token == None: 
      # update existing profile
      profile = user.profile
      addNewProfile = False
    else:
      #create new profile
      profile = Profile()
      addNewProfile = True
    profile.password_reset_token = uuid.uuid4()
    profile.password_reset_token_expiration = timezone.now()
    if addNewProfile == True:
      user.profile = profile
    profile.save() # save profile 
    user.save() # save user
    # send confirmation email
    send_mail(
      'Reset password Keydex',
      'http://' + request.META['HTTP_HOST'] + '/users/token/' + str(profile.password_reset_token),
      'do-not-reply@keydex.com',
      [user.email],
      fail_silently=False,
    )
    return redirect('main_index')

def change_password(request, token):
  if request.method == 'GET':
    # render form to ask new password
    form = ChangePasswordForm()
    return render(request, 'change_password.html', { 'form': form })
  else:  # request.method == 'POST'
    if (request.POST['password'] != request.POST['password_repeated']):
      # passwords dont match
      return redirect('users_reset_password') 
    profile = Profile.objects.get(password_reset_token=token)
    if profile == None:
      # token not valid
      return redirect('users_reset_password') 
    user = User.objects.get(profile=profile)
    user.set_password(request.POST['password'])
    user.save()
    user.profile.password_reset_token = None
    user.profile.password_reset_token_expiration = None
    user.profile.save()
    return redirect('main_index')

def save_product(request):
  return render(request, 'step_2.html')
