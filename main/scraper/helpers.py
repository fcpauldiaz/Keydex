# -*- coding: utf-8 -*-
import os
import random
from datetime import datetime
from urlparse import urlparse
import requests

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

import settings
import json

num_requests = 0

def get_proxy():
    # choose a proxy server to use for this request, if we need one
    new_proxy = json.loads(requests.get('https://api.getproxylist.com/proxy?protocol=http&allowsHttps=1&apiKey=' + settings.PROXY_API_KEY).content)
    if ('ip' in new_proxy):
        proxy = {
            'http': str(new_proxy['ip']) + ':' + str(new_proxy['port']),
            'https': str(new_proxy['ip']) + ':' + str(new_proxy['port'])
        }
        return proxy
    return {
        'http': '108.59.14.208:13041',
        'https': '108.59.14.208:13041'
    }

def make_request_with_proxy(asin, host, keyword, proxy, retries):
    if (retries == 1):
        return None, None
    try:
        s = requests.Session()
        url = host+"/s/ref=nb_sb_noss_2?url=search-alias%3Daps&"
        params = asin
        if keyword != None:
            params += " " + keyword.strip()
        querystring = {"field-keywords": params }

        headers = {
            'cache-control': "no-cache",
            'user-agent': random.choice(settings.USER_AGENTS)['User-Agent']
        }
        r = s.get(url, headers=headers, params=querystring, proxies=proxy)
        #print r.url
    except RequestException as e:
        #log("WARNING: Request for {} {} failed, trying again.".format(url, querystring))
        message = str(e.message)
        if (message.find('Connection aborted') != 1 or message.find('BadStatusLine') != -1):
            #use another proxy service
            proxy = get_proxy()
            if (proxy != None):
                return make_request_with_proxy(asin, host, keyword, proxy, retries+1)

        return None, None

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        log("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
        return None, None

    return BeautifulSoup(r.content, 'lxml'), r.content


def make_request(asin, host, keyword=None, return_soup=True):
    # global request building and response handling

    #url = format_url(url)

    global num_requests
    if num_requests >= settings.max_requests:
        raise Exception("Reached the max number of requests: {}".format(settings.max_requests))

    #proxies = get_proxy()
    try:
        s = requests.Session()
        url = host+"/s/"
        params = asin
        if keyword != None:
            params += " " + keyword.strip()
        querystring = {"field-keywords": params }

        headers = {
            'cache-control': "no-cache",
            'user-agent': random.choice(settings.USER_AGENTS)['User-Agent']
        }
        
        r = s.get(url, headers=headers, params=querystring, proxies=get_proxy())
        print r.url
    except RequestException as e:
        #log("WARNING: Request for {} {} failed, trying again.".format(url, querystring))
        message = str(e.message)
        log("WARNING: Request for {} {} {} failed, trying again.".format(url, querystring, message))
        if (message.find('Connection aborted') != 1 or message.find('BadStatusLine') != -1 or message.find('bad handshake') != -1):
            log("USING ANOTHER PROXY")
            #use another proxy service
            proxy = get_proxy()
            if (proxy != None):
                return make_request_with_proxy(asin, host, keyword, proxy, 0)
            
        return None, None
        #return make_request(url)  # try request again, recursively

    num_requests += 1

    if r.status_code != 200:
        os.system('say "Got non-200 Response"')
        log("WARNING: Got a {} status code for URL: {}".format(r.status_code, url))
        return None, None

    if return_soup:
        return BeautifulSoup(r.content, 'lxml'), r.content
    return r


def format_url(url):
    # make sure URLs aren't relative, and strip unnecssary query args
    u = urlparse(url)

    scheme = u.scheme or "https"
    host = u.netloc or "www.amazon.com"
    path = u.path
    if not u.query:
        query = ""
    else:
        query = '?'+u.query
        # for piece in u.query.split("&"):
        #     k, v = piece.split("=")
        #     if k in settings.allowed_params:
        #         query += "{k}={v}&".format(**locals())
        # query = query[:-1]

    return "{scheme}://{host}{path}{query}".format(**locals())


def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print "{}: {}".format(datetime.now(), msg)
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text




def enqueue_url(u):
    url = format_url(u)
    return redis.sadd("listing_url_queue", url)


def dequeue_url():
    return redis.spop("listing_url_queue")

def chooseHeader(header):
    header['User-Agent'] = random.choice(settings.USER_AGENTS)['User-Agent']
    return header


if __name__ == '__main__':
    # test proxy server IP masking
    r = make_request('https://api.ipify.org?format=json', return_soup=False)
    print r.text
