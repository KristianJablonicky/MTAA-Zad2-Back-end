"""
Definition of urls for MTAA_z2.
"""

from datetime import datetime
from django.urls import path
from django.urls import re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from app import forms, views

import datetime

urlpatterns = [
    path('home', views.home, name='home/'),
    #POST
    re_path(r'^postUser/W/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?:date=(?P<birth_date>[0-9/-]+)/)?(?:email=(?P<email>[^//]+)/)?(?:phone=(?P<phone>[0-9/+]+)/)?$', views.post_worker), 
    re_path(r'^postUser/E/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<companyName>[^//\d]+)/(?:date=(?P<birth_date>[0-9/-]+)/)?(?:email=(?P<email>[^//]+)/)?(?:phone=(?P<phone>[0-9/+]+)/)?$', views.post_employer), 
    re_path(r'^postCompany/(?P<name>[^//\d]+)/(?P<email>[^//]+)/(?P<phone>[0-9/+]+)/(?:web=(?P<website>[^//]+)/)?(?:detail=(?P<detail>[^//]+)/)?$', views.post_company),
    re_path(r'^postJobOffer/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<job_name>[^//\d]+)/(?P<field>[^//\d]+)/(?:salary=(?P<salary>\d+)/)?(?:hours=(?P<working_hours>[0-9:]+)/)?(?:location=(?P<location>[^//]+)/)?(?:detail=(?P<detail>[^//]+)/)?$', views.post_jobOffer),
    re_path(r'^postApplication/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<id>\d+)/(?:desc=(?P<description>[^//]*)/)?(?:expires=(?P<expires_on>[0-9:/-]+)/)?$', views.post_application),
    re_path(r'^postCall/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<employer_id>\d+)/(?P<worker_id>\d+)/(?:name=(?P<callName>[^//\d]+)/)?$', views.post_call),
    path('postPDF/<str:name>/<str:password>/', views.postPDF),
    #DELETE
    path('delUser/<str:type>/<str:name>/<str:password>/', views.delete_user),
    path('delJobOffer/<str:name>/<str:password>/<int:id>/', views.delete_jobOffer),
    path('delApplication/<str:name>/<str:password>/<int:id>/', views.delete_application),
    #GET
    re_path(r'^findUsers/((?P<type>.)/$)?$', views.get_all_users),
    path('getUser/<str:name>/<str:password>/', views.login_user),
    path('getWorker/<int:id>/', views.get_worker),
    path('getEmployer/<int:id>/', views.get_employer),
    path('getJobOffer/<int:id>/', views.get_job_offer),
    path('getCompany/<int:id>/', views.get_company),
    path('getAllApplications/<str:type>/<int:id>/', views.get_all_applications),
    path('getAllJobOffers/<int:employerID>/', views.get_all_job_offers),
    path('getAllEmployers/<int:companyID>/', views.get_all_employers),
    path('getAllCalls/<str:type>/<int:id>/', views.get_all_calls),
    path('searchJobOffers/', views.search_Jobs),
    path('getPDF/<int:id>/', views.getPDF),

    #PUT
    re_path(r'^putJobOffer/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<id>\d+)/(?:name=(?P<jobName>[^//\d]+)/)?(?:field=(?P<field>[^//\d]+)/)?(?:salary=(?P<salary>\d*)/)?(?:hours=(?P<working_hours>[0-9:]*)/)?(?:location=(?P<location>[^//]*)/)?(?:detail=(?P<detail>[^//]*)/)?$', views.put_job_offer),
    re_path(r'^putCall/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<id>\d+)/(?:name=(?P<callName>[^//\d]+)/)?(?:status=(?P<status>[a-zA-Z]+)/)?$', views.put_call),
    re_path(r'^putWorker/(?P<oldName>[^//\d]+)/(?P<oldPassword>[^//]+)/(?P<id>\d+)/(?:name=(?P<name>[^//\d]+)/)?(?:password=(?P<password>[^//]+)/)?(?:date=(?P<birth_date>[0-9/-]*)/)?(?:email=(?P<email>[^//]*)/)?(?:phone=(?P<phone>[0-9/+]*)/)?$', views.put_worker),
    re_path(r'^putEmployer/(?P<oldName>[^//\d]+)/(?P<oldPassword>[^//]+)/(?P<id>\d+)/(?:name=(?P<name>[^//\d]+)/)?(?:password=(?P<password>[^//]+)/)?(?:date=(?P<birth_date>[0-9/-]*)/)?(?:email=(?P<email>[^//]*)/)?(?:phone=(?P<phone>[0-9/+]*)/)?(?:company=(?P<companyId>[0-9]+)/)?$', views.put_employer),
    path('putApplication/E/<str:name>/<str:password>/<int:id>/<str:response>', views.put_applicationE),
    re_path(r'^putApplication/W/(?P<name>[^//\d]+)/(?P<password>[^//]+)/(?P<id>\d+)/(?:desc=(?P<description>[^//]*)/)?(?:expires=(?P<expires_on>[0-9:/-]+)/)?$', views.put_applicationW),
]