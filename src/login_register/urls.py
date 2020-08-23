from django.urls import path, re_path
from django.conf.urls import url
from . import views


# app_name = 'login_register'

urlpatterns = [

    path('get-user-id/', views.jwt_response_payload_handler, name="get_user"),
    path('^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),    

]