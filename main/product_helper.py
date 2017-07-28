from models import  Keywords, ProductHistoricIndexing

def save_product_indexing(result, product):
  indexed = 0.0
  indexing_data = {}
  keyword_length = 0
  for keyword, indexing in result.items():
    keyword_entity = Keywords(
      keyword=keyword,
      indexing=indexing,
      product=product
    )
    keyword_entity.save()
    if (indexing == True):
      indexed += 1
    keyword_length += 1
  indexing_rate = float(indexed)/float(keyword_length) * 100
  historic_entity = ProductHistoricIndexing(
    indexing_rate=indexing_rate,
    product=product
  )
  #save transactional operation
  historic_entity.save()

def delete_session(request):
  del request.session['keywords']
  del request.session['product']

def datetime_handler(x):
  if isinstance(x, datetime):
      return x.isoformat()
  raise TypeError("Unknown type")

def select_email_reporting(value1, value2):
  if (value1 == "type5"):
    return 100
  if value2 == "type7":
    return 95
  if value2 == "type8":
    return 80
  if value2 == "type9":
    return 70
  if value2 == "type10":
    return 50
  raise TypeError("Unknown Email Reporting")
