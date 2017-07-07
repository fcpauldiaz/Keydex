from django.shortcuts import render
from forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
  return render(
    request,
    'index.html'
  )

def loginUser(request):
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
          'index.html'
        )
    else:
      #not valid credentials
      return render(
        request,
        'index.html'
      )
  else:
    "other method"

def createUser(request):
  message = ''
  if request.method == 'GET':
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

