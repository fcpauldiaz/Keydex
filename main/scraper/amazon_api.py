# -*- coding: utf-8 -*-
from amazon.api import AmazonAPI
from models import ProductRecord
from datetime import datetime
import settings
from time import sleep, time
from random import uniform

#function to retrieve a product information
#on a given marketplace
def amazon_api(asin, url, marketplace = 'US', retries=0):
  try:
    if (retries < 2):
      amazon = AmazonAPI(settings.AWS_KEY_1, settings.AWS_SECRET_1, settings.AWS_API_1, region=marketplace)
    if (retries >= 2 and retries < 4):
      amazon = AmazonAPI(settings.AWS_KEY_2, settings.AWS_SECRET_2, settings.AWS_API_2, region=marketplace)
    if (retries >= 4 and retries < 6):
      amazon = AmazonAPI(settings.AWS_KEY_3, settings.AWS_SECRET_3, settings.AWS_API_3, region=marketplace)
    if (retries >= 6 and retries < 8):
      amazon = AmazonAPI(settings.AWS_KEY_3, settings.AWS_SECRET_3, settings.AWS_API_4, region=marketplace)
    if (retries >= 8 and retries < 10):
      amazon = AmazonAPI(settings.AWS_KEY_3, settings.AWS_SECRET_3, settings.AWS_API_5, region=marketplace)
    product = amazon.lookup(ItemId=asin)
    model_product = ProductRecord(
      title=product.title,
      product_url='<missing product url>',
      listing_url=url,
      price=str(product.price_and_currency[1])+str(product.price_and_currency[0]),
      primary_img=product.large_image_url,
      product_indexing=None,
      crawl_time=datetime.now(),
      asin=asin.upper()
    )
    if (product.asin != asin):
      return None
    return model_product
  except Exception as e:
    if (retries <= 10):
      return amazon_api(asin, url, marketplace, retries+1)
    return None

#function to retrieve if a product is indexing
#on a given marketplace with a keyword
def amazon_product(asin, keyword, marketplace = 'US', retries=0):  
  try:
    if (retries < 2):
      amazon = AmazonAPI(settings.AWS_KEY_1, settings.AWS_SECRET_1, settings.AWS_API_1, region=marketplace)
    if (retries >= 2 and retries < 4):
      amazon = AmazonAPI(settings.AWS_KEY_2, settings.AWS_SECRET_2, settings.AWS_API_2, region=marketplace)
    if (retries >= 4 and retries < 6):
      amazon = AmazonAPI(settings.AWS_KEY_3, settings.AWS_SECRET_3, settings.AWS_API_3, region=marketplace)
    if (retries >= 6 and retries < 8):
      amazon = AmazonAPI(settings.AWS_KEY_3, settings.AWS_SECRET_3, settings.AWS_API_3, region=marketplace)
    if (retries >= 8 and retries < 10):
      amazon = AmazonAPI(settings.AWS_KEY_4, settings.AWS_SECRET_4, settings.AWS_API_4, region=marketplace)
    if (retries >= 10 and retries < 12):
      amazon = AmazonAPI(settings.AWS_KEY_4, settings.AWS_SECRET_4, settings.AWS_API_5, region=marketplace)
    if (retries >= 12 and retries < 16):
      amazon = AmazonAPI(settings.AWS_KEY_6, settings.AWS_SECRET_6, settings.AWS_API_6, region=marketplace)
    if (retries >= 16):
      return 'Information Not Available'

    search_item = asin + ' ' + keyword
    products = amazon.search_n(1, Keywords=search_item, SearchIndex='All')
    if len(products) != 0:
      if (products[0].asin != asin):
        return 'Information Not Available'
      return True
    return False
  except Exception as e:
    if str(e) == 'HTTP Error 503: Service Unavailable':
      sleep(1 + uniform(0, retries))
      return amazon_product(asin, keyword, marketplace, retries+1)
    if str(e) == 'HTTP Error 403: Forbidden':
      sleep(1)
      return amazon_product(asin, keyword, marketplace, retries+1)
    return False  

#print amazon_product('B00OQVZDJM', 'kindle', 'US', 15)

