"""
Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from app.models import *

from datetime import datetime
import json
import requests

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

#GET
@require_http_methods(["GET"])
def get_all_users(request): 

    workers = Worker.objects.all()

    employers = Employer.objects.all()

    
    dict = list(workers.values()) + list(employers.values())

    return HttpResponse(json.dumps(dict, indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def login_user(request, name, password):

    users = Worker.objects.filter(name = name,password = password)

    if not users:
        users = Employer.objects.filter(name = name,password = password)

    if not users:
        return HttpResponse("Zle zadané prihlasovacie údaje!", status=204)

    return HttpResponse(json.dumps(list(users.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_worker(request, id):

    workers = Worker.objects.filter(id = id)

    if not workers:
        return HttpResponse("Robotník sa nenašiel.", status=204)

    return HttpResponse(json.dumps(list(workers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_employer(request, id):

    Employers = Employer.objects.filter(id = id)

    if not Employers:
        return HttpResponse("Zamestnávateľ sa nenašiel.", status=204)

    return HttpResponse(json.dumps(list(Employers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_employers(request, companyID):

    Employers = Employer.objects.filter(company_id = companyID)

    if not Employers:
        return HttpResponse("SPoločnosť nemá žiadnych zamestnancov.", status=204)

    return HttpResponse(json.dumps(list(Employers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_company(request, id):

    Companies = Company.objects.filter(id = id)

    if not Companies:
        return HttpResponse("Spoločnosť sa nenašla.", status=204)

    return HttpResponse(json.dumps(list(Companies.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_job_offer(request, id):

    Offers = JobOffer.objects.filter(id = id)

    if not Offers:
        return HttpResponse("Pracovná ponuka sa nenašla.", status=204)

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_job_offers(request, employerID):

    Offers = JobOffer.objects.filter(employer_id = employerID)

    if not Offers:
        return HttpResponse("Neexistujú žiadne pracovné ponuky zamestnávateľa.", status=204)

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_calls (request, type, id):

    if type == 'W':
        Calls = Call.objects.filter(worker_id = id)

    elif type == 'E':
        Calls = Call.objects.filter(employer_id = id)

    else:
        return HttpResponse("Zadal si zlý typ používateľa.", status= 400)

    if not Calls:
        return HttpResponse("História hovorov je prázdna.", status=204)

    return HttpResponse(json.dumps(list(Calls.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_applications (request, type, id):

    if type == 'W':
        Applications = Application.objects.filter(worker_id = id)

    elif type == 'J':
        Applications = Application.objects.filter(job_offer_id = id)

    else:
        return HttpResponse("Zadal si zlý typ používateľa.", status= 400)

    if not Applications:
        return HttpResponse("Pracovník nemá žiadne požiadavky.", status=204)

    return HttpResponse(json.dumps(list(Applications.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def search_Jobs (request):

    Offers = JobOffer.objects.all()

    if not Offers:
        return HttpResponse("Neexistujú žiadne pracovné ponuky.", status=204)

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")

#PUT
@require_http_methods(["PUT"])
def put_worker (request, id, name, password, birth_date, email, phone, cv):

    if (not name) or (not password):
        return HttpResponse("Chybné údaje robotníka.", status=400)

    worker = Worker.objects.get (pk = id)

    if not worker:
        return HttpResponse("Robotník sa nenašiel.", status=404)

    worker.name = name
    worker.password = password
    worker.birth_date = birth_date
    worker.email = email
    worker.phone = phone
    #doplnit ukladanie pdf
    #worker.cv = ....

    worker.save()
    return HttpResponse("Robotnik bol úspešne uložený.", status=200)

@require_http_methods(["PUT"])
def put_employer (request, id, name, password, birth_date, email, phone, companyName):

    if (not name) or (not password):
        return HttpResponse("Chybné údaje zamestnávateľa.", status=400)

    employer = Employer.objects.get (pk = id)

    if not employer:
        return HttpResponse("Zamestnávateľ sa nenašiel.", status = 404)

    company = Company.objects.get(name = companyName)

    if (not company) and companyName:
        return HttpResponse("Meno spoločnosti sa nenašlo.", status = 404)


    employer.name = name
    employer.password = password
    employer.birth_date = birth_date
    employer.email = email
    employer.phone = phone
    employer.company_id = company.id

    employer.save()
    return HttpResponse("Zamestnávateľ bol úspešne uložený.", status=200)

@require_http_methods(["PUT"])
def put_call (request, userID, id, name, status):

    if (not name) or (not status):
        return HttpResponse("Chybné údaje hovoru.", status=400)

    call = Call.objects.get (pk = id)

    if not call:
        return HttpResponse("Hovor sa nenašiel.", status = 404)

    if (userID != call.worker_id) and  (userID != call.employer_id):
        return HttpResponse("Hovor možu meniť iba jeho účastníci.", status = 401)

    call.name = name
    call.status = status

    call.save()
    return HttpResponse("Hovor bol úspešne uložený.", status=200)

@require_http_methods(["PUT"])
def put_job_offer (request, employerID, id, name, field, salary, working_hours, location, detail):

    offer = JobOffer.objects.get(pk = id)

    if not offer:
        return HttpResponse("Pracovná ponuka sa nenašla.", status = 404)

    if employerID != offer.employer_id:
        return HttpResponse("Pracovnú ponuku možu meniť iba jej vlastník.", status = 401)

    offer.name = name
    offer.field = field
    offer.salary = salary
    offer.working_hours = working_hours
    offer.location = location
    offer.detail = detail

    offer.save()
    return HttpResponse("Pracovná ponuka bola úspešne uložená.", status=200)

@require_http_methods(["PUT"])
def put_applicationE (request , employerID, id , response):

    application = Application.objects.get(pk = id)

    if not application:
        return HttpResponse("Žiadosť sa nenašla.", status = 404)

    offer = JobOffer.objects.get(pk = application.job_offer_id)

    if not offer:
        return HttpResponse("Pracovná ponuka žiadosti sa nenašla.", status = 404)

    if offer.employer_id != employerID:
        return HttpResponse("Na žiadosť može odpovedať iba vlastník pracovnej ponuky žiadosti.", status = 401)

    application.response = response

    application.save()
    return HttpResponse("Odpoveď na žiadosť bola úspešne uložená.", status=200)

@require_http_methods(["PUT"])
def put_applicationW (request , workerID, id , description, expires_on):

    application = Application.objects.get(pk = id)

    if not application:
        return HttpResponse("Žiadosť sa nenašla.", status = 404)

    if application.worker_id != workerID:
        return HttpResponse("Žiadosť može meniž iba jej podateľ.", status = 401)

    application.description = description
    application.expires_on = expires_on

    application.save()
    return HttpResponse("Žiadosť bola úspešne uložená.", status=200)

#POST
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

        return HttpResponse(returnValue, status=201)
    else:
        return HttpResponse("request.method != POST", status=400)

def postCompany (request, company):
    if request.method == 'POST':
        newCompany = Company(name = company, phone = 'tel.Cislo', email = 'e-mail')
        newCompany.save()
        return HttpResponse("Firma bola pridaná do databázy", status=201)
    else:
        return HttpResponse("postCompany.method != POST", status=400)

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

        return HttpResponse(returnValue, status=201)
    else:
        return HttpResponse("request.method != POST", status=400)

def test1_w (request, type, name, password):

    r = requests.post('http://127.0.0.1:8000/postUser/' + type + '/' + name + '/' + password)
    return HttpResponse(r.text, status=200)

def test1_e (request, type, name, password, company):
    r = requests.post('http://127.0.0.1:8000/postUser/' + type + '/' + name + '/' + password + '/' + company)
    return HttpResponse(r.text, status=200)

def postJobOffer (request, name, employer_id, field, salary, working_hours, location, detail):
    if request.method == 'POST':
        newOffer = JobOffer(name=name, employer_id=employer_id, field=field, salary=salary, working_hours=working_hours, location=location, detail=detail)
        newOffer.save()
        return HttpResponse("postJobOffer bol uspesny", status=201)
    else:
        return HttpResponse("postJobOffer nie je POST", status=400)

def testJobOffer (request):
    r = requests.post('http://127.0.0.1:8000/postJobOffer/' + 'TestMeno/12/TestField/800/00:08/TestLocation/testtesttestdetail')
    return HttpResponse(r.text, status=200)

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
        return HttpResponse("postApplication nie je POST", status=400)

    return HttpResponse("postApplication bol uspesny", status=201)

def testApplication (request):
    r = requests.post('http://127.0.0.1:8000/postApplication/' + '1/1/som pracoviti/1528797322/1528797340')
    return HttpResponse(r.text, status=200)

def postCall (request, employer_id, worker_id):
    if request.method == 'POST':

        queryJobName = JobOffer.objects.raw('SELECT id, name FROM job_offer WHERE employer_id = \'' + str(employer_id) + '\';')
        
        newCall = Call(employer_id = employer_id, worker_id = worker_id, name = queryJobName[0].name + ' Call', status = False)
        newCall.save()
    else:
        return HttpResponse("postCall nie je POST", status=400)

    return HttpResponse("postCall bol uspesny", status=201)

def testCall (request):
    r = requests.post('http://127.0.0.1:8000/postCall/1/4')
    return HttpResponse(r.text, status=200)

#DELETE
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
            return HttpResponse("Nesprávny formát! Používateľ nie je ani Worker, ani Employer", status=400)

    else:
        return HttpResponse("deleteUser nie je DELETE", status=400)

    return HttpResponse("deleteUser bol úspešný.", status=200)

def testDeleteUser (request):
    r = requests.delete('http://127.0.0.1:8000/deleteUser/E/12')
    return HttpResponse(r.text, status=200)

def deleteJobOffer (request, job_offer_id):
    if request.method == 'DELETE':
        Application.objects.filter(job_offer_id=job_offer_id).delete() # vymazanie applications viazucich sa na mazanu pracovnu ponuku
        JobOffer.objects.filter(id=job_offer_id).delete()
    else:
        return HttpResponse("deleteJobOffer nie je DELETE", status=400)
    return HttpResponse("deleteJobOffer bol úspešný", status=200)

def testDeleteJobOffer (request):
    r = requests.delete('http://127.0.0.1:8000/deleteJobOffer/6')
    return HttpResponse(r.text, status=200)
