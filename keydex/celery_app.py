from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from django.contrib.auth.models import User
from calendar import monthrange
from main.models import Product, Keywords, ProductHistoricIndexing
from main.scraper.crawler import cron_crawler
from django.core.mail import send_mail
from django.template import loader

import unicodedata 
import datetime
import requests
import time
import os

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keydex.settings')

app = Celery('keydex')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def last_day_month(today):
  dict_range = monthrange(today.year, today.month)
  if dict_range[1] == today.day:
      return True
  return False

def weekend(today):
  if today.weekday() == 6:
      return True
  return False

def send_email(asin_list, user):

  first_name = user.first_name
  last_name = user.last_name
  email_format = first_name + ' ' + last_name + '<' + user.email + '>'
  html_message = loader.render_to_string(
  'email_reporting.html',
    {
      'asin_list': asin_list,
      'first_name': first_name,
      'last_name': last_name
    }
  )
  
  message = 'Your keywords report'
  subject = "Your Keyword's Report"
  from_email = 'Check My Keywords <do-not-reply@mail.checkmykeywords.com>'
  send_mail(subject,message,from_email,[email_format],fail_silently=True,html_message=html_message)

def save_product_indexing(result, product):
  indexed = 0.0
  indexing_data = {}
  keyword_length = 0
  entities = []
  for keyword, indexing in result.items():
    keyword_entity = Keywords(
      keyword=keyword,
      indexing=indexing
    ) 
    #save in memory
    entities.append(keyword_entity)
    if (indexing == True):
      indexed += 1
    keyword_length += 1
  indexing_rate = float(indexed)/float(keyword_length) * 100
  historic_entity = ProductHistoricIndexing(
    indexing_rate=indexing_rate,
    product=product
  )
  #save transactional operation
  historic_entity.save()
  #finish save of keywords
  for entity in entities:
    entity.historic = historic_entity
    entity.save()
  return historic_entity.id

@app.task
def cron_job():
  users = User.objects.filter(profile__account_confirmed=True)
  message = ''
  for user in users:
    asins_to_email = []
    id_user = user.id
    products = Product.objects.filter(user=user)
    failed = False
    for product in products:
      periodicity = product.reporting_period
      reporting_percentage = product.reporting_percentage
      today = datetime.date.today()
      asin = product.asin
      if (periodicity == 'monthly'):
        #check if today is endof month
        monthly = last_day_month(today)
        if (monthly == False):
            continue
      elif (periodicity == 'weekly'):
          #check if today is sunday
          sunday = weekend(today)
          if (sunday == False):
              continue
      elif (periodicity == '-1'):
          continue
      rDict = cron_crawler(product, product.marketplace)
      save_product_indexing(rDict, product)
      if reporting_percentage >= 100:
          #save in memory for email later
          asins_to_email.append(asin)
      elif reporting_percentage >= rate:
          #save in memory for email later
          asins_to_email.append(asin)
    if len(asins_to_email) != 0:
      #print 'Sending email ' + user_email
      send_email(asins_to_email, user)
      asins_to_email = []  
  return failed

