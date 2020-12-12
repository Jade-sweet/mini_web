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
from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import HouseInfoViewSet, user_login, user_register, user_logout, get_image, new_image, get_log, \
    find_password, change_password, get_user_info, change_user_tel

urlpatterns = [
    path('token/', user_login),
    path('new_user/', user_register),
    path('invalid_token/', user_logout),
    path('user_image/', get_image),
    path('get_user_info/', get_user_info),
    path('new_image/', new_image),
    path('logs/', get_log),
    path('find_password/', find_password),
    path('new_password/', change_password),
    path('change_user_tel/', change_user_tel),
]
router = SimpleRouter()
router.register('houseinfos', HouseInfoViewSet)
urlpatterns += router.urls

