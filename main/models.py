from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
import uuid


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)
  instance.profile.save()

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  account_confirmed = models.BooleanField(default=False)
  password_reset_token = models.CharField(max_length=150, null=True)
  password_reset_token_expiration = models.DateTimeField(null=True) 
  billing_address = models.CharField(max_length=120, null=True)


class ReportingPeriod(models.Model):
  #text to show user
  text = models.CharField(max_length=100)
  #value to query for
  value = models.CharField(max_length=100, unique=True)
  #hour to run cron.
  datetime = models.TimeField()
  #yearly, monthly, weekly, daily
  periodicity = models.CharField(max_length=100)
  #day of the week
  day_of_week = models.CharField(max_length=10)

  def __unicode__( self ):
    return self.text

  class Meta:
    db_table = 'main_reporting_period'

class Marketplace(models.Model):
  country = models.CharField(max_length=100)
  #US, DE, FR, UK 
  country_code = models.CharField(max_length=10)
  #country url
  country_host = models.CharField(max_length=100)
  #css option
  disabled = models.BooleanField(default=True)

  def render_css(self):
    return { 'label': self.country, 'disabled': self.disabled }
  def __unicode__( self ):
    return self.country

class Product(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  asin = models.CharField(max_length=40)
  product_name = models.CharField(max_length=500)
  product_url = models.CharField(max_length=2056)
  listing_url = models.CharField(max_length=2056)
  price = models.CharField(max_length=128)
  primary_img = models.CharField(max_length=2056)
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  keywords = ArrayField(models.CharField(max_length=1000), null=True)
  phrases = ArrayField(models.CharField(max_length=1000), null=True)
  reporting_period = models.ForeignKey(ReportingPeriod)
  marketplace = models.ForeignKey(Marketplace)
  reporting_percentage = models.DecimalField(decimal_places=2, max_digits=5)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)

  @property
  def indexing(self):
    historic_list = ProductHistoricIndexing.objects.filter(product=self.id).last()
    if (historic_list == None):
      return '0%'
    rate = historic_list.indexing_rate
    indexing_data = format(rate, '.0f')
    return indexing_data+'%'

class ProductHistoricIndexing(models.Model):
  product = models.ForeignKey(Product)
  indexing_rate = models.DecimalField(max_digits=5, decimal_places=2)
  indexed_date = models.DateTimeField(auto_now_add=True) 
  class Meta:
    db_table = 'main_product_historic_indexing'

class Keywords(models.Model):
  keyword = models.CharField(max_length=1000)
  indexing = models.CharField(max_length=30)
  index_date = models.DateTimeField(auto_now_add=True)
  historic = models.ForeignKey(ProductHistoricIndexing, related_name="historic_keywords", null=True)

class Subscription(models.Model):
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  valid_subscription = models.BooleanField()
  trialUser = models.BooleanField()
  creditCard = models.CharField(max_length=19)
  expiration_card_date = models.CharField(max_length=5)
  security_code = models.CharField(max_length=5)
  billing_address = models.CharField(max_length=100)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)
  

class HistoricSubscription(models.Model):
  subscription = models.ForeignKey(Subscription, null=True, on_delete=models.SET_NULL)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)
