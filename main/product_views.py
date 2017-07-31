from django.shortcuts import render, redirect, reverse
from forms import AsinForm, ProductSave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from models import Profile, Product, ReportingPeriod, Keywords, ProductHistoricIndexing
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from scraper.crawler import begin_crawl, fetch_listing
from product_helper import *
import uuid
import json

@login_required
def add_product(request):
  if request.method == 'POST':
    form = AsinForm(request.POST)
    if form.is_valid():
      asin = request.POST['asin']
      return redirect('products_add_keywords', asin=asin)
    return render(request, 'step_1.html', {'form': form}) 
  elif request.method == 'GET':
    form = AsinForm()
    return render(request, 'step_1.html', {'form': form})
  raise ValueError('Invalid request at add product')

@login_required
def add_keywords(request, asin):
  if request.method == 'GET':
    asin = asin.strip()
    product = fetch_listing(asin)
    if (product == None): #not parseable
      redirect('products_add_product')
    request.session['product'] = json.dumps(product.__dict__, default=datetime_handler)
    return render(request, 'step_2.html', {'product':product})
  elif request.method == 'POST':
    data = request.POST.get('chips', [])
    request.session['keywords'] = data
    return JsonResponse({ 'data': data })
  raise ValueError('Invalid request at add keywords')
  

@login_required
def save_product(request):
  try:
    data = {
      'keywords': request.session['keywords'],
      'product': request.session['product']
    }
  except:
    #no longer product in session
    return redirect('products_add_product')
  if request.method == 'GET':
    form = ProductSave()
    return render(request, 'step_3.html', { 'form': form })
  
  elif request.method == 'POST':
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
      product = Product.objects.create(
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
      product.save()
      #run indexing
      if 'saveAndRun' in request.POST:
        result = begin_crawl(product)
        save_product_indexing(result, product)
        #delete session variables not longer used
        delete_session(request)
        return redirect('products_detail_product', uuid=product.uuid)  
      delete_session(request)
      return redirect('dashboard')

    else:
      return render(request, 'step_3.html', { 'form': form })
  raise ValueError('Invalid request at save product')

@login_required
def product_detail(request, uuid):
  #check if user has permission to see this prodcut
  product = Product.objects.get(uuid=uuid)
  #user created this product
  if (product.user_id == request.user.id):
    historic = ProductHistoricIndexing.objects.get(product=product, indexed_date=datetime.now().date())
    print historic
    keywords = Keywords.objects.filter(product=product).order_by('-indexing')
    op = float(historic.indexing_rate)
    indexing_data = {}
    indexing_data['indexed'] = format(op, '.2f')
    indexing_data['not_indexed'] = format(100 - op, '.2f')
    indexing_data['count'] = len(keywords)
    indexing_data['indexed_count'] = int(round(op/100*len(keywords)))
    indexing_data['not_indexed_count'] = len(keywords) - int(round(op/100*len(keywords)))
    data =  { 
      'product': product,
      'keywords': keywords,
      'indexing_data': indexing_data
    }
    return render(request, 'product_detail.html', data)
  return render(request, 'product_detail.html')

def datetime_handler(x):
  if isinstance(x, datetime):
      return x.isoformat()
  raise TypeError("Unknown type")