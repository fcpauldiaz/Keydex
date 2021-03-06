from models import  Keywords, ProductHistoricIndexing, Product
from pinax.stripe.actions import subscriptions
from pinax.stripe.models import Customer

def check_valid_subscription(user):
  products = Product.objects.filter(user=user).count()
  if (products < 5):
    return True
  customer = Customer.objects.filter(user_id=user).first()
  valid_subscription = False
  if customer != None:
    valid_subscription = subscriptions.has_active_subscription(customer=customer)
  return valid_subscription

def save_product_indexing(result, product):
  indexed = 0.0
  indexing_data = {}
  keyword_length = 0
  entities = []
  for value in result:
    keyword = value.keys()[0]
    indexing = value.values()[0]
    keyword_entity = Keywords(
      keyword=keyword,
      indexing=indexing
    ) 
    #save in memory
    entities.append(keyword_entity)
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
  #finish save of keywords
  for entity in entities:
    entity.historic = historic_entity
    entity.save()
  return historic_entity.id
  
def calculate_indexing(indexing_rate, keyword_length):
  indexing_data = {}
  indexing_data['indexed'] = format(indexing_rate, '.2f')
  indexing_data['not_indexed'] = format(100 - indexing_rate, '.2f')
  indexing_data['count'] = keyword_length
  indexing_data['indexed_count'] = int(round(indexing_rate/100*keyword_length))
  indexing_data['not_indexed_count'] = keyword_length - int(round(indexing_rate/100*keyword_length))
  return indexing_data


#delete session temporal data
def delete_session(request):
  del request.session['keywords']
  del request.session['product']
  del request.session['marketplace']


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
