from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
  password_reset_token = models.CharField(max_length=150, null=True)
  password_reset_token_expiration = models.DateTimeField(null=True) 

class HistoricProducts(models.Model):
  index_date = models.DateTimeField()
  index_rate = models.DecimalField(decimal_places=2, max_digits=3)

class Product(models.Model):
  asin = models.CharField(max_length=40)
  user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
  keywords = ArrayField(models.CharField(max_length=100))
  reporting_period = models.CharField(max_length=100)
  reporting_percentage = models.DecimalField(decimal_places=2, max_digits=3)
  historic_ref = models.ForeignKey(HistoricProducts, null=True, on_delete=models.SET_NULL)
  createdAt = models.DateTimeField(auto_now_add=True)
  updatedAt = models.DateTimeField(auto_now=True)
  
  
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
