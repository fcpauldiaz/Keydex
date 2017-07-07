from django.conf.urls import url
from main import views as main_views

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
    name='users_logout_user')
]