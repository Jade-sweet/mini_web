"""test_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from common.views import spider_start, get_county, get_street, spider_info, check_login, get_tel_code, map_info, \
    login_img

urlpatterns = [
    path('spider/', spider_start),
    path('county_list/', get_county),
    path('street_list/', get_street),
    path('spider_info/', spider_info),
    path('check_login/', check_login),
    path('tel_code/', get_tel_code),
    path('map_info/', map_info),
    path('login_img/', login_img),
]
