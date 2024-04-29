
from django.contrib import admin

from django.urls import path

from django.conf import settings

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('pages/dashboard.html', views.dashboard, name='dashboard'),
    path('pages/ecozlounge.html', views.ecozlounge, name='ecozlounge'),
    path('pages/bba.html', views.bba, name='bba'),
]