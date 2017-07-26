from django.conf.urls import url
from main import views as main_views
from main import product_views

urlpatterns = [
  url(
    r'^$',
    main_views.index,
    name='main_index'),
  url(
    r'^user/create$',
    main_views.createUser,
    name='users_create_user'),
  url(
    r'^user/login$',
    main_views.loginUser,
    name='users_login_user'),
  url(
    r'^user/logout$',
    main_views.logout_view,
    name='users_logout_user'),
  url(
    r'^user/reset/password$',
    main_views.reset_password,
    name='users_reset_password'),
  url(
    r'^user/change/password/(?P<token>[0-9A-Za-z-]+)', 
    main_views.change_password,
    name='users_change_password'
  ),
  url(
    r'^product/add', 
    product_views.add_product,
    name='products_add_product'
  ),
  url(
    r'^product/keywords/(?P<asin>[0-9A-Za-z-]+)', 
    product_views.add_keywords,
    name='products_add_keywords'
  ),
  url(
    r'^product/save/', 
    product_views.save_product,
    name='products_save_product'
  ),

]