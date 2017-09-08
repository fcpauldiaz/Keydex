from __future__ import absolute_import, unicode_literals
from celery import shared_task, current_task
from main.scraper import helpers   #make_request
from main.scraper.extractors import get_title, get_url, get_price, get_primary_img, get_indexing
from time import sleep

@shared_task
def index_data(asin, country_host, keywords_and_phrases, retries):
  returnDictionary = {}
  total = float(len(keywords_and_phrases))
  for index, keyword in enumerate(keywords_and_phrases):
    process_percent = float(index)/total
    current_task.update_state(state='PROGRESS', meta={ 'process_percent': process_percent })
    page, html = helpers.make_request(asin=asin, host=country_host, keyword=keyword)
    if page == None:
        #log("WARNING: Error in {} found in the extraction. keyword {}".format(product.asin, keyword))
        sleep(2)
        #if (retries < 3):
          #return index_data(product, marketplace, keyword, retries + 1)
        returnDictionary[keyword] = 'Information not available'
        #product_indexing = amazon_product(product.asin, keyword, marketplace.country_code)
        #returnDictionary[keyword] = product_indexing
    else:    
        item = page
        product_indexing = get_indexing(item)
        returnDictionary[keyword] = product_indexing
      #print returnDictionary
  return returnDictionary
  #output.put(returnDictionary)
  #return '{} random users created with success!'.format(total)