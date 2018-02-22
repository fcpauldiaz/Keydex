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
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file
from django.http import JsonResponse

import uuid
from pinax.referrals.models import Referral
from user_helper import validate_email #email validation
from django.views.defaults import page_not_found, server_error
from django.template.response import TemplateResponse



from models import Profile, Product
from tokens import account_activation_token



def index(request):
  if request.user.is_authenticated():
    return redirect('dashboard')
  return render(
    request,
    'keywords/index.html'
  )

def tutorial(request):
  if request.user.is_authenticated() == False:
    return redirect('dashboard')
  return render(
    request,
    'tutorial.html'
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
    try:
      username_or_email = request.POST['username_or_email'].lower().strip()
      user_object = User.objects.filter(username = username_or_email) | User.objects.filter(email = username_or_email)
      user_object = user_object[0]
    except:
      errors=form.add_error("username_or_email", "Username or email not found")
      return render(
        request,
        'login.html', { 'form': form }
      )
    user = authenticate(
      username=user_object.username.lower().strip(),
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
          errors=form.add_error("username_or_email", "Please click on the email we sent you to verify your account.")
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
      #validate user email
      email = user_form.cleaned_data['email']
      mail_response = validate_email(email)
      
      disposable = mail_response['is_disposable_address'] #disposable
      if (disposable == True):
        errors=user_form.add_error("email", "Email " + str(email) + " seems to be disposable, use another one.")
        data = { 'user_form': user_form }
        return render(request,'sign_up.html', data)
      

      user = user_form.save(commit=False)
      user.is_active = False
      user.username = user.username.lower().strip()
      user.save()
      referral_response = Referral.record_response(request, "SIGN_UP", target=user)
      send_confirmation_email(request, user)
      return render(request, 'account_activation_sent.html', { 'email': email })
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
      username_or_email = request.POST['username_or_email'].lower().strip()
      user = User.objects.filter(username = username_or_email) | User.objects.filter(email = username_or_email)
      user = user[0]
    except:
      errors=form.add_error("", "User not found")
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
        send_reset_email(request, user)
        messages.success(request, 'Reset password email sent.')
        return redirect('main_index')
      else:
        errors=form.add_error("", "The recover link has already been requested")
        data = { 'form': form }
        # wait one hour before ask for another reset password token
        return render(request, 'reset_password.html', data) 
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
    user.save() # save userp
    # send confirmation email
    send_reset_email(request, user)
    messages.success(request, 'Reset password email sent.')
    return redirect('main_index')

def change_password(request, token):
  if request.method == 'GET':
    # render form to ask new password
    form = ChangePasswordForm()
    return render(request, 'change_password.html', { 'form': form })
  else:  # request.method == 'POST'
    if (request.POST['password'] != request.POST['password_repeated']):
      # passwords dont match
      form = ChangePasswordForm(request.POST)
      messages.error(request, 'Password does not match')
      return render(request, 'change_password.html', { 'form': form })
    profile = Profile.objects.filter(password_reset_token=token).first()
    if profile == None:
      messages.error(request, 'Token not found, try again.')
      # token not valid
      return redirect('users_reset_password') 
    user = User.objects.get(profile=profile)
    user.set_password(request.POST['password'])
    user.save()
    user.profile.password_reset_token = None
    user.profile.password_reset_token_expiration = None
    user.profile.save()
    messages.success(request, 'Password has been updated')
    return redirect('users_login_user')


def send_confirmation_email(request, user):
  current_site = get_current_site(request)
  uid = urlsafe_base64_encode(force_bytes(user.pk))
  token = account_activation_token.make_token(user)
  html_message = loader.render_to_string(
    'account_activation_email.html',
    {
      'user': user,
      'domain': request.META['HTTP_HOST'],
      'uid': uid,
      'token': token,
      'referral_link': user.profile.referral.url
    }
  )
  
  message = 'http://' + request.META['HTTP_HOST'] + '/activate/' + str(uid) + '/' + str(token)
  subject = 'Thank you for signing up! '
  from_email = 'Check My Keywords <do-not-reply@mail.checkmykeywords.com>'
  msg = EmailMultiAlternatives(
    subject=subject,
    body=message,
    from_email=from_email,
    to=[user.first_name + ' ' + user.last_name + '<' + user.email +'>'],
    reply_to=["Support <support@checkmykeywords.com>"])

  # Include an inline image in the html:

  html = html_message
  msg.attach_alternative(html, "text/html")

  # Optional Anymail extensions:
  msg.metadata = {"user_id": request.user.id }
  msg.tags = ["confirmation_email"]
  msg.track_clicks = True
  # Send it:
  msg.send()


def send_reset_email(request, user):
  current_site = get_current_site(request).domain
  reset_url = 'https://'+ 'checkmykeywords.com' + '/user/change/password/' + str(user.profile.password_reset_token)
  message = reset_url
  subject = 'Reset your password'
  from_email = 'Check My Keywords <do-not-reply@mail.checkmykeywords.com>'
  html_message = loader.render_to_string(
    'account_reset_email.html',
    {
      'user': user,
      'reset_url': reset_url
    }
  )
  msg = EmailMultiAlternatives(
    subject=subject,
    body=message,
    from_email=from_email,
    to=[user.first_name + ' ' + user.last_name + '<' + user.email +'>'],
    reply_to=["Support <support@checkmykeywords.com>"])

  # Include an inline image in the html:
  
  html = html_message
  msg.attach_alternative(html, "text/html")

  # Optional Anymail extensions:
  msg.metadata = {"user_id": request.user.id }
  msg.tags = ["reset_email"]
  msg.track_clicks = True

  # Send it:
  msg.send()
 
  
  


def account_activation_sent(request):
  return render(request, 'account_activation_sent.html')

#activate a user's account after confirming email
#
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
    return redirect('tutorial')
  else:
    return render(request, 'account_activation_invalid.html')

def check_username(request):
  if request.is_ajax():
    username_to_check = request.POST['username']
    exists = User.objects.filter(username=username_to_check).first()
    if (exists == None):
      return JsonResponse(True, safe=False) #valid
    return JsonResponse(False, safe=False) #not valid

def server_error(request, template_name='500.html'):
    """500 error handler using RequestContext."""
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != '500.html':
            # Reraise if it's a missing custom template.
            raise
        return http.HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    return http.HttpResponseServerError(template.render(None, request, status=500))
