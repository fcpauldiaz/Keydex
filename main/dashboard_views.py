from django.shortcuts import render, redirect, reverse
from models import Profile, Product, ReportingPeriod, Keywords
from django.contrib.auth.decorators import login_required

def dashboard(request):
  products = Product.objects.filter(user=request.user)
  data = { 'products': products }
  return render(request, 'dashboard.html', data)
