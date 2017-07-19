from django.shortcuts import render, redirect, reverse
from forms import AsinForm, ProductSave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from models import Profile, Product, ReportingPeriod, Keywords
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.template import loader
from django.http import JsonResponse
from django.forms import formset_factory
from scraper.crawler import begin_crawl, fetch_listing
import uuid
import json

@login_required
def add_product(request):
  if request.method == 'POST':
    form = AsinForm(request.POST)
    if form.is_valid():
      asin = request.POST['asin']
      return redirect('keywords/?q=%s' % asin )
    return render(request, 'step_1.html', {'form': form}) 
  else:
    form = AsinForm()
    return render(request, 'step_1.html', {'form': form})

# def add_product(request):
#   if request.method == 'POST':
#     if request.POST['action'] == "+":
#       extra = int(float(request.POST['extra'])) + 1
#       form = AsinForm(initial=request.POST)
#       formset = formset_factory(FormsetForm, extra=extra)
#     else:
#       extra = int(float(request.POST['extra']))
#       form = AsinForm(request.POST)
#       formset = formset_factory(FormsetForm, extra=extra)(request.POST)

#       # if form.is_valid() and formset.is_valid():
#       #   if request.POST['action'] == "Create":
#       #     for form_c in formset:
#       #         if not form_c.cleaned_data['delete']:
#       #             # create data
#       #   elif request.POST['action'] == "Edit":
#       #     for form_c in formset:
#       #         if form_c.cleaned_data['delete']:
#       #             # delete data
#       #         else:
#       #               # create data
#           # return HttpResponseRedirect('abm_usuarios')
#   form = AsinForm()
#   extra = 1
#   formset = formset_factory(FormsetForm, extra=extra)
  
#   return render(request, 'step_1.html', {'form': formset})

@login_required
def add_keywords(request):
  if request.method == 'GET':
    asin = request.GET['q']
    asin = asin.strip()
    product = fetch_listing(asin)
    print product, "product"
    request.session['product'] = json.dumps(product.__dict__, default=datetime_handler)
    return render(request, 'step_2.html', {'product':product})
  else:
    data = request.POST.get('chips', [])
    request.session['keywords'] = data
    return JsonResponse({'data': data})
  

@login_required
def save_product(request):
 
  data = {
    'keywords': request.session['keywords'],
    'product': request.session['product']
  }
  if request.method == 'GET':
    form = ProductSave()
    return render(request, 'step_3.html', { 'form': form })
  #request.method == 'POST'
  else:
    form = ProductSave(request.POST)
    if form.is_valid():
      value_report = form.cleaned_data['choices_group1']
      reporting_period = ReportingPeriod.objects.get(value=value_report)
      percentage_report = select_email_reporting(
        form.cleaned_data['choices_group2'],  
        form.cleaned_data['choices_group3']
      )
      product_json = json.loads(data['product'])
      keywords = json.loads(data['keywords'])
      product = Product(
        asin= product_json['asin'],
        product_name= product_json['title'],
        product_url= product_json['product_url'],
        price= product_json['price'],
        primary_img= product_json['primary_img'],
        keywords=keywords,
        reporting_period=reporting_period,
        reporting_percentage=percentage_report,
        user=request.user
      )
      product_id = product.save() 
      if 'saveAndRun' in request.POST:
        result = begin_crawl(product)
        for keyword, indexing in result.items():
          keyword_entity = Keywords(
            keyword=keyword,
            indexing=indexing,
            product=product
          )
          keyword_entity.save()
      return redirect('main_index');

    else:
      return render(request, 'step_3.html', { 'form': form })


def datetime_handler(x):
  if isinstance(x, datetime):
      return x.isoformat()
  raise TypeError("Unknown type")

def select_email_reporting(value1, value2):
  if (value1 == "type5"):
    return 100
  if value2 == "type7":
    return 95
  if value2 == "type8":
    return 80
  if value2 == "type9":
    return 70
  if value2 == "type10":
    return 50
  raise TypeError("Unknown Email Reporting")
