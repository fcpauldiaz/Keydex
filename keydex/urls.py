"""keydex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.defaults import page_not_found, server_error
from django.template.response import TemplateResponse

def handler500(request):
  """500 error handler which includes ``request`` in the context.

  Templates: `500.html`
  Context: None
  """

  context = {'request': request}
  template_name = '500.html'  # You need to create a 500.html template.
  return TemplateResponse(request, template_name, context, status=500)


urlpatterns = [
  url(r'^indexer/', admin.site.urls),
  url(r'^', include('main.urls')),
  #url(r"^payments/", include("pinax.stripe.urls")),  
]
