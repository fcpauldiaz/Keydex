from django.shortcuts import render, redirect, HttpResponseRedirect
from forms import SignUpForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils import timezone, http
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
      return redirect('products_add_product')
  #to redirect after login to other view
  redirect_to = None
  if (next in request.GET):
    redirect_to = request.GET['next']

  if request.method == 'GET':
    form = LoginForm()
    return render(
      request,
      'login.html',
      {
        'form': form
      }
    )
  else:
   #request.method == 'POST':
    form = LoginForm(request.POST)
    user = authenticate(
      username=request.POST['username'],
      password=request.POST['password'],
    )
    if redirect_to != None:
      return HttpResponseRedirect(next)
    if user is not None:
        login(request, user)
        return redirect('products_add_product')
    #not valid credentials
    return render(
      request,
      'login.html',
      {
          'form': form
      }
    )

def createUser(request):
  message = ''
  if request.method == 'GET':
      user_form = SignUpForm()

  elif request.method == 'POST':
    user_form = SignUpForm(request.POST)
    message = "User created successfully"
    if user_form.is_valid():
      user = User.objects.create_user(
        request.POST['username'],
        request.POST['email'],
        request.POST['password']
      )
      user.first_name = request.POST['first_name']
      user.last_name = request.POST['last_name']
      user.save()
      auth_user = authenticate(
        username=user.username,
        password=request.POST['password'],
      )
      login(request, auth_user)
      return redirect('products_add_product')
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
  return redirect('main_index')

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
      'http://' + request.META['HTTP_HOST'] + '/user/change/password/' + str(profile.password_reset_token),
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


def send_html_email(request):
  html_message = loader.render_to_string(
      'path/to/your/htm_file.html',
      {
        'user_name': user.name,
        'subject':  'Thank you from' 
      }
  )
  send_mail(subject,message,from_email,to_list,fail_silently=True,html_message=html_message)
