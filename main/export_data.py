from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from models import  Keywords, ProductHistoricIndexing, Product
from django.contrib.auth.decorators import login_required
from product_helper import calculate_indexing
import django_excel as excel

@login_required
def export_excel(request, uuid, historic_id):
  #check if user has permission to see this prodcut
  product = Product.objects.get(uuid=uuid)
  #user created this product
  if (product.user_id == request.user.id):
    data = []
    historic = ProductHistoricIndexing.objects.get(id=urlsafe_base64_decode(force_text(historic_id)))
    keywords = Keywords.objects.filter(historic=historic).order_by('-indexing')
    column_names = [
      '#',
      'keyword or phrase',
      'indexed'
    ]
    data.append(column_names)
    for index, keyword in enumerate(keywords):
      new_row = []
      new_row.extend((index, keyword.keyword, keyword.indexing))
      data.append(new_row)
    sheet = excel.pe.Sheet(data)
    sheet.name = "Check My Keywords"
    return excel.make_response(sheet, "xlsx",  file_name="export_data")

