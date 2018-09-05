from __future__ import absolute_import, unicode_literals
import datetime
import main.scraper.settings
from main.scraper.models import ProductRecord
from main.scraper.helpers import make_request, log, format_url, enqueue_url, dequeue_url
from main.scraper.extractors import get_title, get_url, get_price, get_primary_img, get_indexing
from main.scraper.amazon_api import amazon_api, amazon_product
from django.core import serializers
from time import sleep, time
from ..tasks import index_data, paralel_data
import json
import billiard as mp
from random import randint

crawl_time = datetime.datetime.now()

def cron_crawler(product, marketplace):
    final_dict = {}
    if product.phrases == None:
        keywords_and_phrases = product.keywords
    else:
        keywords_and_phrases = product.keywords + product.phrases
    for keyword in keywords_and_phrases:
        res = single_crawl(product, marketplace, keyword, 0)
        final_dict.update(res)
    return final_dict

def single_crawl(product, marketplace, keyword, retries):
    returnDictionary = {}
    sleep(randint(1, 10))
    page, html = make_request(asin=product.asin, host=marketplace.country_host, keyword=keyword)
    if page == None:
        #log("WARNING: Error in {} found in the extraction. keyword {}".format(product.asin, keyword))
        sleep(randint(1, 10))
        if (retries < 2):
            return single_crawl(product, marketplace, keyword, retries + 1)
         #returnDictionary[keyword] = 'Information not available'
        product_indexing = amazon_product(product.asin, keyword, marketplace.country_code)
        returnDictionary[keyword] = product_indexing
        #log("WARNING: ENTRA API 1")
    else:    
        item = page
        product_indexing = get_indexing(item)
        if (product_indexing == None):
            #log("WARNING: ENTRA API 2")
            product_indexing = amazon_product(product.asin, keyword, marketplace.country_code)
        returnDictionary[keyword] = product_indexing
    return returnDictionary
    
def begin_crawl(product, marketplace, keyword, retries, output):
    returnDictionary = {}
    sleep(randint(1, 10))
    page, html = make_request(asin=product.asin, host=marketplace.country_host, keyword=keyword)
    if page == None:
        #log("WARNING: Error in {} found in the extraction. keyword {}".format(product.asin, keyword))
        sleep(randint(1, 10))
        if (retries < 3):
            return begin_crawl(product, marketplace, keyword, retries + 1, output)
        #returnDictionary[keyword] = 'Information not available'
        product_indexing = amazon_product(product.asin, keyword, marketplace.country_code)
        returnDictionary[keyword] = product_indexing
    else:    
        item = page
        product_indexing = get_indexing(item)
        if (product_indexing == None):
            product_indexing = amazon_product(product.asin, keyword, marketplace.country_code)
        returnDictionary[keyword] = product_indexing
    #return returnDictionary
    output.put(returnDictionary)

def queue_crawl(product, marketplace):
    if product.phrases == None:
        keywords_and_phrases = product.keywords
    else:
        keywords_and_phrases = product.keywords + product.phrases
    job = paralel_data(product.asin, marketplace.country_host, marketplace.country_code, keywords_and_phrases, 0)
    return job

def parallel_crawl(product, marketplace):
    if product.phrases == None:
        keywords_and_phrases = product.keywords
    else:
        keywords_and_phrases = product.keywords + product.phrases
    # Define an output queue
    output_queue = mp.Queue()
    # Setup a list of processes that we want to run
    processes = [mp.Process(target=begin_crawl, args=(product, marketplace, keyword, 0, output_queue)) for keyword in keywords_and_phrases]
    #intial_time = time()
    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()
    # Get process results from the output queue
    results = [output_queue.get() for p in processes]
    #final_time = time()
    return dict(pair for d in results for pair in d.items())

def fetch_listing(ASIN, marketplace):

    global crawl_time
    url = marketplace.country_host+"/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+ASIN
    if not url:
        log("WARNING: No URLs {} found in the queue. Retrying...".format(url))
        #pile.spawn(fetch_listing)
        return

    page, html = make_request(ASIN, marketplace.country_host)
    if not page:
        log("WARNING: No page. Retrying")
        #sleep(3)
        #fetch_listing(ASIN, marketplace)
    if page == None:
        return amazon_api(ASIN, url, marketplace.country_code)
    item = page
    product_image = get_primary_img(item)
    if not product_image:
        log("No product image detected, skipping")
        # continue
    product_title = get_title(item)
    product_url = get_url(item)
    product_price = get_price(item)
    product_indexing = get_indexing(item)
    if (product_title == '<missing product title>' and 
        product_url == '<missing product url>'):
        product = amazon_api(ASIN, url, marketplace.country_code)
    else:
        product = ProductRecord(
            title=product_title,
            product_url=format_url(product_url),
            listing_url=format_url(url),
            price=product_price,
            primary_img=product_image,
            product_indexing=product_indexing,
            crawl_time=crawl_time,
            asin=ASIN
        ) 
    return product

def datetime_handler(x):
  if isinstance(x, datetime.datetime):
      return x.isoformat()
  raise TypeError("Unknown type")
