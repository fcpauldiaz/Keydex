from pinax.stripe.models import Customer, Card, Plan, Coupon
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from pinax.stripe.actions.sources import create_card, update_card
from pinax.stripe.actions import subscriptions, customers
from django.http import JsonResponse
from django.dispatch import receiver
from pinax.stripe.signals import WEBHOOK_SIGNALS

import stripe
import json


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
      created_at=data['created'],
      percent_off=data['percent_off'],
      amount_off=data['amount_off'],
      currency=data['currency'],
      duration=data['duration'],
      duration_in_months=data['duration_in_months'],
      livemode=data['livemode'],
      max_redemptions=data['max_redemptions'],
      redeem_by=data['redeem_by'],
      times_redeemed=data['times_redeemed'],
      valid=data['valid']
    )
    cp.save()
    print cp
  pass  # do what it is you want to do here

@receiver(WEBHOOK_SIGNALS["coupon.deleted"])
def handle_coupon_deleted(sender, event, **kwargs):
  if event.valid == True:
    data = event.validated_message['data']['object']
    cp = Coupon.objects.get(
      stripe_id=data['id']
    )
    cp.remove()
  pass  # do what i
