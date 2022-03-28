"""
Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict

from datetime import datetime
import json

import requests
import datetime
from datetime import datetime

from app.models import *

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def get_all_users(request): 

    #ORM query
    users = Worker.objects.all()

    #RAW query 
    users_raw = Worker.objects.raw('SELECT * from worker')

    #serializing ORM or RAW query to json
    #note: creates extra fields
    data = serializers.serialize('json', users_raw)

    #ORM query as directory (doesnt work on RAW query)
    dict = list(users.values())

    return HttpResponse(json.dumps(dict, indent = 4, default=str), content_type="application/json")

def post_worker (request, type, name, password):

    if request.method == 'POST':

        returnValue = "Používateľ " + name + " nebol úspešne vytvorený!"
        
        if type == 'W':
            query = Worker.objects.raw('SELECT id, name FROM worker where name = \'' + name + '\';') # kontrola, ci dane meno este nie je v databaze

            if not query:
                newWorker = Worker(name=name, password=password)
                newWorker.save()
                returnValue = "Používateľ " + name + " bol úspešne vytvorený."

            else:
                print("Pouzivatel s menom ", name, " uz existuje")
        else:
            print("worker nema type W")

        return HttpResponse(returnValue)
    else:
        return HttpResponse("request.method != POST")

def postCompany (request, company):
    if request.method == 'POST':
        newCompany = Company(name = company, phone = 'tel.Cislo', email = 'e-mail')
        newCompany.save()
        return HttpResponse("Firma bola pridaná do databázy")
    else:
        return HttpResponse("postCompany nebol post :O")

def post_employer (request, type, name, password, company):

    if request.method == 'POST':

        returnValue = "Používateľ " + name + " nebol úspešne vytvorený!"
        
        if type == 'E':
            queryName = Employer.objects.raw('SELECT id, name FROM employer where name = \'' + name + '\';')
            queryCompany = Employer.objects.raw('SELECT id FROM company where name = \'' + company + '\';')
            
            if not queryName:

                if queryCompany:

                    print("--ID: " + str(queryCompany[0].id))

                    newWorker = Employer(name=name, password=password, company_id=queryCompany[0].id)
                    newWorker.save()
                    returnValue = "Používateľ " + name + " bol úspešne vytvorený."
                
                else: # company nie je pridana v databaze

                    r = requests.post('http://127.0.0.1:8000/postCompany/' + company)
                    queryCompany = Employer.objects.raw('SELECT id FROM company where name = \'' + company + '\';')

                    newWorker = Employer(name=name, password=password, company_id=queryCompany[0].id)
                    newWorker.save()
                    returnValue = "Používateľ " + name + ", a ich firma bola úspešne vytvorená."
            else:
                print("Pouzivatel s menom ", name, " uz existuje, alebo firma ", company, "nie je v databaze.")
        else:
            print("worker nema type W")

        return HttpResponse(returnValue)
    else:
        return HttpResponse("request.method != POST")



def test1_w (request, type, name, password):

    r = requests.post('http://127.0.0.1:8000/postUser/' + type + '/' + name + '/' + password)
    return HttpResponse(r.text)

def test1_e (request, type, name, password, company):
    r = requests.post('http://127.0.0.1:8000/postUser/' + type + '/' + name + '/' + password + '/' + company)
    return HttpResponse(r.text)

def postJobOffer (request, name, employer_id, field, salary, working_hours, location, detail):
    if request.method == 'POST':
        newOffer = JobOffer(name=name, employer_id=employer_id, field=field, salary=salary, working_hours=working_hours, location=location, detail=detail)
        newOffer.save()
        return HttpResponse("postJobOffer bol uspesny")
    else:
        return HttpResponse("postJobOffer nie je POST")
def testJobOffer (request):
    r = requests.post('http://127.0.0.1:8000/postJobOffer/' + 'TestMeno/12/TestField/800/00:08/TestLocation/testtesttestdetail')
    return HttpResponse(r.text)


def postApplication (request, worker_id, job_offer_id, description, created_on, expires_on):
    if request.method == 'POST':
        query = Application.objects.raw('SELECT id FROM Application WHERE worker_id = ' + str(worker_id) + ' AND job_offer_id = ' + str(job_offer_id) + ';')
        if not query:
            newApplication = Application(worker_id = worker_id, job_offer_id = job_offer_id, description = description,
                                        created_on =  datetime.fromtimestamp(created_on), expires_on =  datetime.fromtimestamp(expires_on))
            newApplication.save()
        else:
            print("Dany Application uz existuje.")
    else:
        return HttpResponse("postApplication nie je POST")

    return HttpResponse("postApplication bol uspesny")

def testApplication (request):
    r = requests.post('http://127.0.0.1:8000/postApplication/' + '1/1/som pracoviti/1528797322/1528797340')
    return HttpResponse(r.text)

def postCall (request, employer_id, worker_id):
    if request.method == 'POST':

        queryJobName = JobOffer.objects.raw('SELECT id, name FROM job_offer WHERE employer_id = \'' + str(employer_id) + '\';')
        
        newCall = Call(employer_id = employer_id, worker_id = worker_id, name = queryJobName[0].name + ' Call', status = False)
        newCall.save()
    else:
        return HttpResponse("postCall nie je POST")

    return HttpResponse("postCall bol uspesny")

def testCall (request):
    r = requests.post('http://127.0.0.1:8000/postCall/1/4')
    return HttpResponse(r.text)

def deleteUser (request, type, user_id):

    if request.method == 'DELETE':
        if type == 'W':
            
            Application.objects.filter(worker_id=user_id).delete() # vymazanie vsetkych Applications worker-a
            Worker.objects.filter(id=user_id).delete() # vymazanie worker-a samotneho
        elif type == 'E':
            
            query = JobOffer.objects.raw('SELECT id FROM job_offer WHERE employer_id =' + str(user_id) + ';') #zistenie idciek JobOffer-ov vytvorenych danym employer-om
            for vysledok in query:
                Application.objects.filter(job_offer_id=vysledok.id).delete()
            JobOffer.objects.filter(employer_id=user_id).delete() # vymazanie vsetkych JobOffers vytvorenych employer-om
            Employer.objects.filter(id=user_id).delete()
        else:
            return HttpResponse("Nesprávny formát! Používateľ nie je ani Worker, ani Employer")

    else:
        return HttpResponse("deleteUser nie je DELETE")

    return HttpResponse("deleteUser bol uspesny.")

def testDeleteUser (request):
    r = requests.delete('http://127.0.0.1:8000/deleteUser/E/12')
    return HttpResponse(r.text)

def deleteJobOffer (request, job_offer_id):
    if request.method == 'DELETE':
        Application.objects.filter(job_offer_id=job_offer_id).delete() # vymazanie applications viazucich sa na mazanu pracovnu ponuku
        JobOffer.objects.filter(id=job_offer_id).delete()
    else:
        return HttpResponse("deleteJobOffer nie je DELETE")
    return HttpResponse("deleteJobOffer bol úspešný")

def testDeleteJobOffer (request):
    r = requests.delete('http://127.0.0.1:8000/deleteJobOffer/6')
    return HttpResponse(r.text)
