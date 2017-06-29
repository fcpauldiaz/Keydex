from django.conf.urls import url
from main import views as main_views

urlpatterns = [
  url(
    r'^$',
    main_views.index,
    name='main_index')
]