from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect, reverse
from main.models import Profile, Product, Keywords, Subscription
from django.contrib.auth.decorators import login_required
from main.scraper.crawler import parallel_crawl, fetch_listing, queue_crawl
from main.product_helper import save_product_indexing
from main.forms import SettingsForm, PlanForm
from django.http import JsonResponse
from pinax.stripe.actions.sources import create_card, update_card
from pinax.stripe.models import Customer, Card
from pinax.stripe.actions import subscriptions
from celery.result import AsyncResult, ResultSet, GroupResult
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from pinax.stripe.actions import subscriptions
from django.contrib import messages

import json
from keydex.celery_app import app

@login_required
def dashboard(request):
  key = settings.PINAX_STRIPE_PUBLIC_KEY
  products = Product.objects.filter(user=request.user)
  customer = Customer.objects.filter(user_id=request.user).first()
  valid_subscription = False
  if customer != None:
    valid_subscription = subscriptions.has_active_subscription(customer=customer)
  form = PlanForm()
  data = { 'products': products, 
    'product_count': len(products), 
    'valid': valid_subscription, 
    'form': form,
    'key': key
  }
  return render(request, 'dashboard.html', data)

@login_required
def check_product_indexing(request, uuid):
  product = Product.objects.get(uuid=uuid)
  job = queue_crawl(product, product.marketplace)  
  request.session['job_total_count'] = len(job.results)
  request.session['job_id'] = job.id
  return redirect(reverse('products_overview_product',kwargs={'uuid':uuid}))


@login_required
def dashboard_settings(request):
  if request.method == 'GET':
    profile = Profile.objects.get(user_id=request.user)
    initial_dict = dict()
    c = Customer.objects.filter(user_id=request.user).first()
    if c == None:
      card = []
    else:
      card = Card.objects.filter(customer_id=c.id)
    data = { 'user': request.user }
    if (len(card) > 0):
      data['last4'] = card[0].last4
      initial_dict['credit_card_name'] = card[0].name

    form = SettingsForm(initial=initial_dict, instance=request.user)
    data['form'] = form 
    return render(request, 'settings.html', data)
  elif request.method == 'POST':
    form = SettingsForm(request.POST, instance=request.user)
    if form.is_valid():
      try:
        form.save()
        data = { 'form': form }
        messages.success(request, 'Saved Successfully!')
        return render(request, 'settings.html', data)
      except:
        data = { 'form': form }
        messages.error(request, 'invalid update')
        return render(request, 'settings.html', data)
    data = { 'form': form }
    messages.error(request, 'Invalid form')
    return render(request, 'settings.html', data)
  raise ValueError('Invalid request type at dashboad settings')

@login_required
def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
      if 'task_id' in request.POST.keys() and request.POST['task_id']:
          task_id = request.POST['task_id']
          task_total = request.POST['task_total']
          task = GroupResult.restore(task_id, app=app)
          progress = task.completed_count()/float(task_total)
          if progress <= 0:
            progress = 0.01
          data = {}
          if progress >= 1.0 and request.session.get('saved') == None:
            request.session['saved'] = 'saved'
            progress = None
            result = task.get()
            task.forget()
            uuid = request.POST['product_uuid']
            p = Product.objects.get(uuid=uuid)
            historic_id = save_product_indexing(result, p)
            data['historic_id'] = urlsafe_base64_encode(force_bytes(historic_id))
            data['uuid'] = str(p.uuid)
          data['process_percent'] = progress 
      else:
          data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'
    
    if isinstance(data, dict):
      data = json.dumps(data)
    return JsonResponse(data, safe=False)
