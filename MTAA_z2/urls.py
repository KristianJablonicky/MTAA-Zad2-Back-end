"""
Definition of urls for MTAA_z2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('users/', views.get_all_users),
]
