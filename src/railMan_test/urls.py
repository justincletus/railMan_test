"""finin_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_view
from login_register.views import signup, home_view
from django.views.generic.base import TemplateView, TemplateResponseMixin, RedirectView
from . import regex
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_auth.views import LogoutView


from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name="home"),    
    re_path('auth/', include('rest_framework.urls')),
    path('rest-auth/logout/', LogoutView, name="rest_logout"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path('signup/', signup, name="signup"),
    path('reg_activate/', include('login_register.urls')),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('movies/', include('movie_rating.urls')),    

]
