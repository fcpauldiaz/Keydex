from django.shortcuts import render, redirect, reverse
from models import Profile, Product, Keywords
from django.contrib.auth.decorators import login_required
from scraper.crawler import begin_crawl, fetch_listing
from product_helper import save_product_indexing

def dashboard(request):
  products = Product.objects.filter(user=request.user)
  data = { 'products': products }
  return render(request, 'dashboard.html', data)

def check_product_indexing(request, uuid):
  product = Product.objects.get(uuid=uuid)
  result = begin_crawl(product)
  save_product_indexing(result, product)
  return redirect(reverse('products_overview_product',kwargs={'uuid':uuid}))



#postgres://checkmykeyword:9ZVwy7GVuD8P5iTbUEwRabJh6@sdb-ts-indexer.cjzyjdlft1jm.us-west-2.rds.amazonaws.com:5432/indexer_ts_db
