from __future__ import absolute_import, unicode_literals
from celery import shared_task, current_task, group
from main.scraper import helpers   #make_request
from main.scraper.extractors import get_title, get_url, get_price, get_primary_img, get_indexing
from main.scraper.amazon_api import amazon_product
from time import sleep

@shared_task
def index_data(asin, country_host, country_code, keyword, retries):
  returnDictionary = {}  
  
  page, html = helpers.make_request(asin=asin, host=country_host, keyword=keyword)
  if page == None:
      #log("WARNING: Error in {} found in the extraction. keyword {}".format(product.asin, keyword))
      sleep(2)
      if (retries < 3):
        return index_data(asin, country_host, country_code, keyword, retries + 1)
      returnDictionary[keyword] = 'Information not available'
      product_indexing = amazon_product(asin, keyword, country_code)
      returnDictionary[keyword] = product_indexing
  else:    
      item = page
      product_indexing = get_indexing(item)
      returnDictionary[keyword] = product_indexing
    #print returnDictionary
  return returnDictionary
  #output.put(returnDictionary)
  #return '{} random users created with success!'.format(total)

def paralel_data(asin, country_host, country_code, keywords_and_phrases, retries):
  tasks = group(index_data.s(asin, country_host, country_code, keyword, retries) for keyword in keywords_and_phrases)
  group_task = tasks.apply_async()
  group_task.save()
  return group_task





