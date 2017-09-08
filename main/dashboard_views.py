from __future__ import absolute_import, unicode_literals
from django.shortcuts import render, redirect, reverse
from main.models import Profile, Product, Keywords
from django.contrib.auth.decorators import login_required
from main.scraper.crawler import parallel_crawl, fetch_listing, queue_crawl
from main.product_helper import save_product_indexing
from main.forms import SettingsForm
from django.http import JsonResponse
from pinax.stripe.actions.sources import create_card, update_card
from pinax.stripe.models import Customer, Card
from pinax.stripe.actions import subscriptions
from celery.result import AsyncResult
import json

@login_required
def dashboard(request):
  products = Product.objects.filter(user=request.user)
  data = { 'products': products }
  return render(request, 'dashboard.html', data)

@login_required
def check_product_indexing(request, uuid):
  product = Product.objects.get(uuid=uuid)
  job = queue_crawl(product, product.marketplace)
  request.session['job_ids'] = job.id
  return redirect(reverse('products_overview_product',kwargs={'uuid':uuid}))


@login_required
def dashboard_settings(request):
  if request.method == 'GET':
    profile = Profile.objects.get(user_id=request.user)
    initial_dict = dict()
    
    if profile.billing_address != None:
      initial_dict = { 'billing_address': profile.billing_address }      
        
    c = Customer.objects.get(user_id=request.user)
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
      form.save()
      profile = Profile.objects.get(user=request.user)
      profile.billing_address = form.cleaned_data['billing_address']
      profile.save()
      customer = Customer.objects.get(user_id=request.user)

      card_dict = json.loads(request.POST.get('token'))
      token = card_dict['id']
      card_user = Card.objects.filter(customer_id=customer.id)
      #check for previous cards for customer
      if (len(card_user) >= 1):
        card_user.delete()
      create_card(customer, token)
      return JsonResponse({'data': 'ok'})
    return JsonResponse({'data': 'not_valid'})
  raise ValueError('Invalid request type at dashboad settings')

def poll_state(request):
    """ A view to report the progress to the user """
    data = 'Fail'
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'
    if data == None:
      return JsonResponse({'finish': True}, safe=False)
    print type(data), 'type'
    if isinstance(data, dict):
      data = json.dumps(data)

    print str(data), 'data'

    return JsonResponse(data, safe=False)
