from django.shortcuts import render, redirect, HttpResponseRedirect
from forms import SignUpForm, LoginForm, ResetPasswordForm, ChangePasswordForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone, http
from datetime import datetime, timedelta
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dateutil.relativedelta import relativedelta
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
import uuid

from models import Profile, Product
from tokens import account_activation_token



def index(request):
  if request.user.is_authenticated():
    return redirect('dashboard')
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
  elif request.method == 'POST':
    form = LoginForm(request.POST)
    user = authenticate(
      username=request.POST['username'].lower(),
      password=request.POST['password'],
    )
    if redirect_to != None:
      return HttpResponseRedirect(next)
    if user is not None:
      login(request, user)
      if hasattr(request.user, 'profile'):
        if (request.user.profile.account_confirmed == True):
          countProducts = Product.objects.filter(user=request.user).count()
          if (countProducts == 0):
            return redirect('products_add_product')
          #else
          return redirect('dashboard')
        else:
          logout(request)
          return render(request, 'login.html', { 'form': form })
    errors=form.add_error("password", "Invalid Credentials")
    return render(
      request,
      'login.html',
      {
        'form': form
      }
    )
  raise ValueError('Invalid request type at login')

def createUser(request):
  if request.method == 'GET':
    user_form = SignUpForm()
    return render(
      request,
      'sign_up.html',
      {
        'user_form': user_form
      }
    )
  elif request.method == 'POST':
    user_form = SignUpForm(request.POST)
    message = "User created successfully"
    if user_form.is_valid():
      user = user_form.save(commit=False)
      user.is_active = False
      user.save()
      current_site = get_current_site(request)
      subject = 'Welcome to CheckMyKeywords'
      message = loader.render_to_string('account_activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
      })
      user.email_user(subject, message)
      return redirect('account_activation_sent')      
    return render(
      request,
      'sign_up.html',
      {
        'user_form': user_form
      }
    )
  raise ValueError('Not valid request at signup')

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
    form = ResetPasswordForm(request.POST)
    try:
      user = User.objects.get(username=request.POST['username'].lower())
    except:
      errors=form.add_error("", "Username " + request.POST['username'] + " not found")
      data = { 'form': form }
      return render(request, 'reset_password.html', data) 


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



def account_activation_sent(request):
  return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
  try:
    uid = force_text(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    user = None

  if user is not None and account_activation_token.check_token(user, token):
    user.is_active = True
    user.profile.account_confirmed = True
    user.save()
    login(request, user)
    return redirect('products_add_product')
  else:
    return render(request, 'account_activation_invalid.html')
