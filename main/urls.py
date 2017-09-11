from django.conf.urls import url
from main import views as main_views
from main import product_views, dashboard_views
from main import export_data as export_views

from django.conf.urls import  handler500 

handler500 = main_views.server_error

urlpatterns = [
  url(
    r'^$',
    main_views.index,
    name='main_index'),
  url(r'^account_activation_sent/$', 
    main_views.account_activation_sent, 
    name='account_activation_sent'),
  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    main_views.activate,
    name='activate'),
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
    r'^product/keywords/(?P<code>[A-Z]{2})/(?P<asin>[0-9A-Za-z-]+)', 
    product_views.add_keywords,
    name='products_add_keywords'
  ),
  url(
    r'^product/save/', 
    product_views.save_product,
    name='products_save_product'
  ),
  url(
    r'^product/edit/(?P<uuid>[0-9A-Za-z-]+)/',
    product_views.edit_product,
    name='products_edit_product'
  ),
   url(
    r'^cron/edit/(?P<uuid>[0-9A-Za-z-]+)/',
    product_views.cron_edit,
    name='products_edit_cron'
  ),
  url(
    r'^product/delete/(?P<pk>\d+)$',
    product_views.delete_product,
    name='products_delete_product'
  ),
  url(
    r'^product/detail/(?P<uuid>[0-9A-Za-z-]+)/(?P<id>[0-9A-Za-z_\-]+)',
    product_views.product_detail,
    name='products_detail_product'
  ),
  url(
    r'^product/export/(?P<uuid>[0-9A-Za-z-]+)/(?P<historic_id>[0-9A-Za-z_\-]+)',
    export_views.export_excel,
    name='products_export_detail'
  ),
  url(
    r'^product/overview/(?P<uuid>[0-9A-Za-z-]+)',
    product_views.product_overview,
    name='products_overview_product'
  ),
  url(
    r'^dashboard/$',
    dashboard_views.dashboard,
    name='dashboard'
  ),
  url(
    r'^dashboard/product/(?P<uuid>[0-9A-Za-z-]+)',
    dashboard_views.check_product_indexing,
    name='dashboard_product_indexing'
  ),
  url(
    r'^settings',
    dashboard_views.dashboard_settings,
    name='dashboard_settings'
  ),
  url(
    r'^poll_state',
    dashboard_views.poll_state,
    name='poll_state'
  ),
]