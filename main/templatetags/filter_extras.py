from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def title(title):
  if (len(title) > 29):
    title = title[:29]
  return title