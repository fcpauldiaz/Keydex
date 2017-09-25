from django.shortcuts import render, redirect, reverse
from forms import AsinForm, ProductSave
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from models import Profile, Product, ReportingPeriod, Keywords, ProductHistoricIndexing, Marketplace
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from scraper.crawler import fetch_listing, parallel_crawl, queue_crawl
from product_helper import *
from collections import namedtuple
from django.contrib import messages
import uuid
import json

@login_required
def add_product(request):
  if request.method == 'POST':
    form = AsinForm(request.POST)
    if form.is_valid():
      asin = form.cleaned_data['asin']
      code = form.cleaned_data['select_choices'].country_code   
      find_repeated = Product.objects.filter(user=request.user, asin=asin).first()
      if find_repeated != None:
        messages.error(request, 'Product already added on dashboard')
        marketplace = Marketplace.objects.all()
        data = { 'form': form, 'urls': marketplace }
        return render(request, 'step_1.html', data) 

      try:
        return redirect('products_add_keywords', asin=asin, code=code)
      except:
        messages.error(request, 'Invalid ASIN')
        marketplace = Marketplace.objects.all()
        data = { 'form': form, 'urls': marketplace }
        return render(request, 'step_1.html', data) 

    marketplace = Marketplace.objects.all()
    data = { 'form': form, 'urls': marketplace }
    return render(request, 'step_1.html', data) 
  elif request.method == 'GET':
    form = AsinForm()
    marketplace = Marketplace.objects.all()
    product_count = Product.objects.filter(user=request.user).count()
    if (product_count >= 500):
      messages.error(request, 'You have reached your product limit')
      return redirect('dashboard')
    data = { 'form': form, 'urls': marketplace }
    return render(request, 'step_1.html', data)
  raise ValueError('Invalid request at add product')

@login_required
def add_keywords(request, code, asin):
  if request.method == 'GET':
    asin = asin.strip()
    marketplace = Marketplace.objects.get(country_code=code)
    product = fetch_listing(asin, marketplace)
    
    if (product == None): #not parseable or not found
      print 'Product not found ' + asin
      return redirect('products_add_product')
    request.session['product'] = json.dumps(product.__dict__, default=datetime_handler)
    dictionary = marketplace.__dict__
    del dictionary['_state'] #delete object from dictionary to serialize
    request.session['marketplace'] = json.dumps(dictionary)
    return render(request, 'step_2.html', {'product':product, 'marketplace': marketplace })
  
  elif request.method == 'POST':
  
    data_key = request.POST.get('chips_keywords', [])
    data_phrase = request.POST.get('chips_phrases', [])
    request.session['keywords'] = data_key
    request.session['phrases'] = data_phrase
    return JsonResponse({ 'data_key': data_key, 'data_phrase': data_phrase})
  
  raise ValueError('Invalid request at add keywords')
  

@login_required
def save_product(request):
  try:
    data = {
      'keywords': request.session['keywords'],
      'phrases': request.session['phrases'],
      'product': request.session['product'],
      'marketplace': request.session['marketplace']
    }
    if request.session.get('saved') != None:
      del request.session['saved']
  except:
    #no longer product in session
    return redirect('products_add_product')
  if request.method == 'GET':
    form = ProductSave()
    return render(request, 'step_3.html', { 'form': form })
  
  elif request.method == 'POST':
    form = ProductSave(request.POST)
    
    if form.is_valid():
      reporting_period = form.cleaned_data['choices_group1']
      percentage_report = select_email_reporting(
        form.cleaned_data['choices_group2'],  
        form.cleaned_data['choices_group3']
      )
      product_json = json.loads(data['product'])
      keywords = json.loads(data['keywords'])
      phrases = json.loads(data['phrases'])
      marketplace = json.loads(data['marketplace'])
      product = Product.objects.create(
        asin= product_json['asin'],
        product_name= product_json['title'],
        product_url= product_json['product_url'],
        price= product_json['price'],
        primary_img= product_json['primary_img'],
        keywords=keywords,
        phrases=phrases,
        reporting_period=reporting_period,
        reporting_percentage=percentage_report,
        user=request.user,
        marketplace=Marketplace.objects.get(id=marketplace['id'])
      )
      product.save()
      #run indexing
      if 'saveAndRun' in request.POST:
        object_market = namedtuple("marketplace", marketplace.keys())(*marketplace.values())
        job = queue_crawl(product, object_market)  
        
        total_job = len(job.results)
        #delete session variables not longer used
        delete_session(request)
        return JsonResponse({ 'uuid': product.uuid, 'job_id': job.id, 'total_job': total_job})
        #return redirect('products_detail_product', uuid=product.uuid, id=urlsafe_base64_encode(force_bytes(historic_id))) 
      delete_session(request)
      return JsonResponse({'saved': True})

    else:
      return render(request, 'step_3.html', { 'form': form })
  raise ValueError('Invalid request at save product')

@login_required
def product_detail(request, uuid, id):
  #check if user has permission to see this prodcut
  product = Product.objects.get(uuid=uuid)
  #user created this product
  if (product.user_id == request.user.id):
    historic = ProductHistoricIndexing.objects.get(id=urlsafe_base64_decode(force_text(id)))
    keywords = Keywords.objects.filter(historic=historic).order_by('-indexing')
    indexing_data = calculate_indexing(historic.indexing_rate, len(keywords))
    data =  { 
      'product': product,
      'keywords': keywords,
      'indexing_data': indexing_data,
      'historic_id': id
    }
    return render(request, 'product_detail.html', data)
  return redirect('dashboard')


@login_required
def product_overview(request, uuid):
  try:
    job_count = request.session['job_total_count']
    task_id = request.session['job_id']
    del request.session['job_total_count']
    del request.session['job_id']
    if request.session.get('saved') != None:
      del request.session['saved']
  except:
    task_id = None
    job_count = -1
    pass
  #check if user has permission to see this prodcut
  product = Product.objects.get(uuid=uuid)
  #user created this product
  if (product.user_id == request.user.id):
    historic = ProductHistoricIndexing.objects.filter(product=product)
    data = { 'data': historic, 'product': product, 'job_count': job_count, 'task_id': task_id }
    return render(request, 'product_overview.html', data)

@login_required
def edit_product(request, uuid):
  product = Product.objects.get(uuid=uuid)
  if request.method == 'GET':
    if (request.user.id == product.user_id):
      data = { 'product': product }
      return render(request, 'product_edit.html', data)
    return redirect('dashboard')
  elif request.method == 'POST':
    keywords_array = request.POST.get('chips_keywords', [])
    phrases_array = request.POST.get('chips_phrases', [])
    request.session['keywords_temp'] = keywords_array
    request.session['phrases_temp'] = phrases_array
    keywords = json.loads(request.session['keywords_temp'])
    phrases = json.loads(request.session['phrases_temp'])
    del request.session['keywords_temp']
    del request.session['phrases_temp']
    product.keywords = keywords
    product.phrases = phrases
    product.save()
    message = 'Product updated'
    data = { 'product': product }
    return JsonResponse({ 'data': True })
  raise ValueError('Invalid request at add keywords')

@login_required
def cron_edit(request, uuid):
  product = Product.objects.get(uuid=uuid)
  if request.method == 'GET':
    if (request.user.id == product.user_id):
      map_group2 = { '100': 'type5'}
      map_group3 = { '95.00': 'type7', '80.00': 'type8', '70.00': 'type9', '50.00': 'type10'}
      group2 = 'type5'
      group3 = ''
      if (product.reporting_percentage != 100):
        group2 = 'type6'
        group3 = map_group3[str(product.reporting_percentage)]


      form = ProductSave(initial={
        'choices_group1': product.reporting_period ,
        'choices_group2': group2,
        'choices_group3': group3
      })
      data = { 'product': product, 'form': form }
      return render(request, 'cron_edit.html', data)
    return redirect('dashboard')
  elif request.method == 'POST':
    form = ProductSave(request.POST)
    if form.is_valid():
      reporting_period = form.cleaned_data['choices_group1']
      percentage_report = select_email_reporting(
        form.cleaned_data['choices_group2'],  
        form.cleaned_data['choices_group3']
      )
      product.reporting_period = reporting_period
      product.reporting_percentage = percentage_report
      product.save()
      messages.success(request, 'Product Updated')
    data = { 'product': product, 'form': form }
    return render(request, 'cron_edit.html', data)
    



@login_required
def delete_product(request, pk):
  if request.method == 'POST':
    p = Product.objects.get(pk=pk)
    if (p.user_id == request.user.id):
      p.delete()
      return redirect('dashboard')
    raise ValueError("Invalid user %s deleting" % (request.user))
  raise ValueError("Invalid request at product delete")

def datetime_handler(x):
  if isinstance(x, datetime):
      return x.isoformat()
  raise TypeError("Unknown type")