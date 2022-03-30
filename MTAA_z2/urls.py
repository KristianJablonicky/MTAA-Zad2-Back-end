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
    path('deleteUser/<str:type>/<int:user_id>', views.deleteUser),
    path('testDeleteUser', views.testDeleteUser),
    path('deleteJobOffer/<int:job_offer_id>', views.deleteJobOffer),
    path('testDeleteJobOffer', views.testDeleteJobOffer),
    path('admin/', admin.site.urls),
    path('findUsers/', views.get_all_users),
    path('getUser/<str:name>/<str:password>/', views.login_user),
    path('getWorker/<int:id>/', views.get_worker),
    path('getJobOffer/<int:id>/', views.get_job_offer),
    path('getEmployer/<int:id>/', views.get_employer),
    path('getCompany/<int:id>/', views.get_company),
    path('getAllApplications/<str:type>/<int:id>/', views.get_all_applications),
    path('getAllJobOffers/<int:employerID>/', views.get_all_job_offers),
    path('getAllEmployers/<int:companyID>/', views.get_all_employers),
    path('getAllCalls/<str:type>/<int:id>/', views.get_all_calls),
    path('findJobOffers/', views.search_Jobs),
    path('putJobOffer/<int:employerID>/<int:id>/<str:name>/<str:field>/<str:salary>/<str:working_hours>/<str:location>/<str:detail>/', views.put_job_offer),
    path('putCall/<int:userID>/<int:id>/<str:name>/<str:status>/', views.put_call),
    path('putWorker/<int:id>/<str:name>/<str:password>/<str:birth_date>/<str:email>/<str:phone>/<str:cv>/', views.put_worker),
    path('putEmployer/<int:id>/<str:name>/<str:password>/<str:birth_date>/<str:email>/<str:phone>/<str:companyName>/', views.put_employer),
    path('putApplication/Employer/<int:employerID>/<int:id>/<str:response>/', views.put_applicationE),
    path('putApplication/Worker/<int:workerID>/<int:id>/<str:description>/<str:expires_on>/', views.put_applicationW),
]
