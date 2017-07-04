from lxml import html  
import csv,os,json
import requests
import random
from exceptions import ValueError
from bs4 import BeautifulSoup
from time import sleep



def AmzonParser(url):
  USER_AGENTS = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0'},
    {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
  ]
  page = requests.get(url,headers=random.choice(USER_AGENTS))
  while True:
    sleep(3)
    try:
      soup = BeautifulSoup(page.content, 'lxml')
      notFound = soup.find('h1', {'id': 'noResultsTitle'})
      return notFound
    except Exception as e:
      print e

def ReadAsin():
  asinList = [
    {
      'asin': 'B00UZKG8QU',
      'keywords': ['popcorn']
    }
  ]
  extracted_data = []
  for i in asinList:
    url = "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="+i['asin']
    for word in i['keywords']:
      url += '+'+word

    print "Processing: "+ url
    result = AmzonParser(url)
    if result == None:
      print 'Keyword is indexing'
    else:
      print 'Keyword is not indexing'
    sleep(5)
  # f=open('data.json','w')
  # json.dump(extracted_data,f,indent=4)

# 'B0046UR4F4',
# 'B00JGTVU5A',
# 'B00GJYCIVK',
# 'B00EPGK7CQ',
# 'B00EPGKA4G',
# 'B00YW5DLB4',
# 'B00KGD0628',
# 'B00O9A48N2',
# 'B00O9A4MEW',
# 'B00UZKG8QU',
if __name__ == "__main__":
    ReadAsin()