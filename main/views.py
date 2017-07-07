from django.shortcuts import render
from forms import SignUpForm

# Create your views here.
def index(request):
  return render(
    request,
    'index.html'
  )

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

