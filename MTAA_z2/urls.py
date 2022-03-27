"""
Definition of urls for MTAA_z2.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from app import forms, views

import datetime

urlpatterns = [
    path('', views.home, name='home'),
    path('test1/<str:type>/<str:name>/<str:password>', views.test1_w), # GET request, ktory vola POST postUser
    path('test1/<str:type>/<str:name>/<str:password>/<str:company>', views.test1_e), # GET request, ktory vola POST postUser
    path('postUser/<str:type>/<str:name>/<str:password>', views.post_worker), # prvotne vytvorenie profilu z login obrazovky
    path('postUser/<str:type>/<str:name>/<str:password>/<str:company>', views.post_employer), # v pripade employera je potrebny nazov firmy kvoli id
    path('postCompany/<str:company>', views.postCompany),
    path('testJobOffer', views.testJobOffer),
    path('postJobOffer/<str:name>/<int:employer_id>/<str:field>/<str:salary>/<str:working_hours>/<str:location>/<str:detail>', views.postJobOffer),
    path('postApplication/<int:worker_id>/<int:job_offer_id>/<str:description>/<int:created_on>/<int:expires_on>', views.postApplication), #worker vytvori application
    path('testApplication', views.testApplication),
    path('postCall/<int:employer_id>/<int:worker_id>', views.postCall),
    path('testCall', views.testCall),
    path('admin/', admin.site.urls),
    path('users/', views.get_all_users),
]
