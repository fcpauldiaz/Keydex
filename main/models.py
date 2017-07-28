from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  account_confirmed = models.BooleanField()
  password_reset_token = models.CharField(max_length=150, null=True)
  password_reset_token_expiration = models.DateTimeField(null=True) 


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

  class Meta:
    db_table = 'main_reporting_period'

class Product(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  asin = models.CharField(max_length=40)
  product_name = models.CharField(max_length=2056)
  product_url = models.CharField(max_length=2056)
  listing_url = models.CharField(max_length=2056)
  price = models.CharField(max_length=128)
  primary_img = models.CharField(max_length=2056)
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  keywords = ArrayField(models.CharField(max_length=100))
  reporting_period = models.ForeignKey(ReportingPeriod)
  reporting_percentage = models.DecimalField(decimal_places=2, max_digits=5)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)

  @property
  def indexing(self):
    keywords = Keywords.objects.filter(product=self.id).order_by('-indexing')
    indexed = 0.0
    indexing_data = {}
    for keyword in keywords:
      if (keyword.indexing == True):
        indexed += 1
    op = float(indexed)/float(len(keywords))*100
    indexing_data = str(op)
    return indexing_data+'%'

  
class Keywords(models.Model):
  keyword = models.CharField(max_length=250)
  indexing = models.BooleanField()
  index_date = models.DateTimeField(auto_now_add=True)
  product = models.ForeignKey(Product, related_name="product_keywords")

class ProductHistoricIndexing(models.Model):
  product = models.ForeignKey(Product)
  indexing_rate = models.DecimalField(max_digits=5, decimal_places=2)
  indexed_date = models.DateField(auto_now_add=True) 
  class Meta:
    db_table = 'main_product_historic_indexing'

class Subscription(models.Model):
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  valid_payment = models.BooleanField()
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
