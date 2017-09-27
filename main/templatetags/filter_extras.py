from django import template
from django.template.defaultfilters import stringfilter
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

register = template.Library()

@register.filter
@stringfilter
def title(title):
  if (len(title) > 35):
    title = title[:35]
  return title

@register.filter
@stringfilter
def product_detail(id):
  return urlsafe_base64_encode(force_bytes(id))

@register.filter
def substract(a, b):
  return a - b