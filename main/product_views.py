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
      return redirect('products_add_keywords', asin=asin)
    return render(request, 'step_1.html', {'form': form}) 
  else:
    form = AsinForm()
    return render(request, 'step_1.html', {'form': form})

@login_required
def add_keywords(request, asin):
  if request.method == 'GET':
    asin = asin.strip()
    print asin, "ASIN"
    product = fetch_listing(asin)
    print product, "product"
    request.session['product'] = json.dumps(product.__dict__, default=datetime_handler)
    print request.session['product']
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
      return redirect('products_detail_product', uuid=product.uuid)

    else:
      return render(request, 'step_3.html', { 'form': form })

@login_required
def product_detail(request, uuid):
  #check if user has permission to see this prodcut
  product = Product.objects.get(uuid=uuid)
  #user created this product
  if (product.user_id == request.user.id):
    keywords = Keywords.objects.filter(product=product).order_by('-indexing')
    indexed = 0.0
    indexing_data = {}
    for keyword in keywords:
      if (keyword.indexing == True):
        indexed += 1
    op = float(indexed)/float(len(keywords))*100
    print op
    indexing_data['indexed'] = format(op, '.2f')
    indexing_data['not_indexed'] = format(100 - op, '.2f')
    indexing_data['count'] = len(keywords)
    indexing_data['indexed_count'] = int(indexed)
    indexing_data['not_indexed_count'] = len(keywords) - int(indexed)
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
