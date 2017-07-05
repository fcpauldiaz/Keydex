from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class User(Document):
    firstName = StringField(max_length=20, required=True)
    lastName = StringField(max_length=20, required=True)
    email = EmailField(max_length=30, required=True)
    password = StringField(max_length=100, required=True)
    createdAt = DateTimeField(required=True, default=datetime.now())
    updatedAt = DateTimeField(required=True, default=datetime.now())
    

class Product(Document):
  ASIN = StringField(max_length=40, required=True)
  user = ReferenceField(User)
  keywords = ListField(StringField(required=True))
  reportingPeriod = StringField()
  reportingPercentage = DecimalField()
  historicRef = ReferenceField(HistoricProducts)
  createdAt = DateTimeField(required=True, default=datetime.now())
  updatedAt = DateTimeField(required=True, default=datetime.now())
  
  meta = {'allow_inheritance': True}

class HistoricProducts(Document):
  indexDate = DateTimeField(required=True)
  indexRate = DecimalField(required=True)
