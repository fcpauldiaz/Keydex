from pinax.stripe.models import Customer, Card, Plan, Coupon
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from pinax.stripe.actions.sources import create_card, update_card
from pinax.stripe.actions import subscriptions, customers
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.dispatch import receiver
from pinax.stripe.signals import WEBHOOK_SIGNALS
from datetime import datetime

import stripe
import json

@login_required
def process_charge(request):
  if request.is_ajax():
    card_dict = json.loads(request.POST.get('token'))
    token = card_dict['id']
    # Charge the user's card:
    customer = Customer.objects.filter(user_id=request.user).first()
    if customer == None:
      customer = customers.create(user=request.user)
    plan = Plan.objects.get(id=request.POST['plan'])
    coupon = request.POST['coupon']
    if coupon == None or coupon == '':
      subs = subscriptions.create(
        customer=customer,
        plan=plan.stripe_id,
        token=token
      )
    else:
      subs = subscriptions.create(
        customer=customer,
        plan=plan.stripe_id,
        token=token,
        coupon=coupon
      )
    valid = subscriptions.is_valid(subs)
  return JsonResponse({'valid': valid })

@login_required
def check_valid_coupon(request):
  if request.is_ajax():
    coupon = request.POST['coupon']
    cp = Coupon.objects.filter(stripe_id=coupon).first()
    if cp == None:
      return JsonResponse({ 'valid_coupon': False })
    if (cp.valid == True):
      plan = Plan.objects.filter(id=request.POST['plan']).first()
      if plan == None:
        return JsonResponse({ 'valid_coupon': False })
      percent = cp.percent_off/100.0
      total = float(plan.amount) - (float(plan.amount) * percent)
      return JsonResponse({ 'valid_coupon': True, 'total_amount': format(total, '.2f') })
    return JsonResponse({ 'valid_coupon': False })




def xstr(s):
  if s is None:
    return 'NA'
  return str(s)

@receiver(WEBHOOK_SIGNALS["invoice.payment_succeeded"])
def handle_payment_succeeded(sender, event, **kwargs):
  print event.kind
  print event.livemode
  print event.customer
  print event.webhook_message
  print event.validated_message
  print event.valid
  print kwargs
  pass  # do what it is you want to do here

@receiver(WEBHOOK_SIGNALS["coupon.created"])
def handle_coupon_created(sender, event, **kwargs):
  if event.valid == True:
    data = event.validated_message['data']['object']
    cp = Coupon(
      stripe_id=data['id'],
      created_at=datetime.fromtimestamp(data['created']),
      percent_off=data['percent_off'],
      amount_off=data['amount_off'],
      currency=xstr(data['currency']),
      duration=data['duration'],
      duration_in_months=data['duration_in_months'],
      livemode=data['livemode'],
      max_redemptions=data['max_redemptions'],
      redeem_by=data['redeem_by'],
      times_redeemed=data['times_redeemed'],
      valid=data['valid']
    )
    cp.save()
  pass  # do what it is you want to do here

@receiver(WEBHOOK_SIGNALS["coupon.deleted"])
def handle_coupon_deleted(sender, event, **kwargs):
  if event.valid == True:
    data = event.validated_message['data']['object']
    cp = Coupon.objects.get(
      stripe_id=data['id']
    )
    cp.delete()
  pass  # do what i
