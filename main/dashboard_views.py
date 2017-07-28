from django.shortcuts import render, redirect, reverse
from models import Profile, Product, ReportingPeriod, Keywords
from django.contrib.auth.decorators import login_required
from scraper.crawler import begin_crawl, fetch_listing
from helper import save_product_indexing
def dashboard(request):
  products = Product.objects.filter(user=request.user)
  products
  data = { 'products': products }
  return render(request, 'dashboard.html', data)

def check_product_indexing(request, uuid):
  product = Product.objects.get(uuid=uuid)
  result = begin_crawl(product)
  save_product_indexing(result, product)
  return redirect('products_detail_product')