"""
Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods
from app.models import *

from datetime import datetime, timedelta
import json
import requests

wrong_type = "ERROR: Wrong user type!"
false_auth = "Data can be altered only by its owner!"
wrong_id = "User could not be found!"
empty_response = "Database does not include any specified data: "
succ_save = "Data has been successfully saved: "
fail_save = "Altered data could not be found: "
succ_delete = "Data has been successfully deleted: "
succ_create = "Data has been created: "
fail_create = "Data already exists: "

def get_id(name, password):

    id = -1

    user = Worker.objects.filter(name = name,password = password)

    if not user:
        user = Employer.objects.filter(name = name,password = password)

    if user:
        id = user[0].id

    return int(id)

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
def get_all_users(request, type='A'): 

    if type != 'W' and type != 'E' and type != 'A':
        return HttpResponse(wrong_type, status=400)

    dict = []

    if type == 'W' or type == 'A':
        workers = Worker.objects.all()
        dict += list(workers.values())

    if type == 'E' or type == 'A':
        employers = Employer.objects.all()
        dict += list(employers.values())
    
    return HttpResponse(json.dumps(dict, indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def login_user(request, name, password): 
    users = Worker.objects.filter(name = name,password = password)

    if not users:
        users = Employer.objects.filter(name = name,password = password)

    if not users:
        if Worker.objects.filter(name = name) or Employer.objects.filter(name = name):
            return HttpResponse("Wrong password", status=204)

        return HttpResponse(empty_response + "User with name = " + name + " and password = " + password, status=204)

    return HttpResponse(json.dumps(list(users.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_worker(request, id):

    workers = Worker.objects.filter(id = id)

    if not workers:
        return HttpResponse(empty_response + "Worker with id = " + str(id), status=204)

    return HttpResponse(json.dumps(list(workers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_employer(request, id):

    Employers = Employer.objects.filter(id = id)

    if not Employers:
        return HttpResponse(empty_response + "Employer with id = " + str(id), status=204)

    return HttpResponse(json.dumps(list(Employers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_employers(request, companyID):

    Employers = Employer.objects.filter(company_id = companyID)

    return HttpResponse(json.dumps(list(Employers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_company(request, id):

    Companies = Company.objects.filter(id = id)

    if not Companies:
        return HttpResponse(empty_response + "Company with id = " + str(id), status=204)

    return HttpResponse(json.dumps(list(Companies.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_job_offer(request, id):

    Offers = JobOffer.objects.filter(id = id)

    if not Offers:
        return HttpResponse(empty_response + "Job offer with id = " + str(id), status=204)

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_job_offers(request, employerID):

    Offers = JobOffer.objects.filter(employer_id = employerID)

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_calls (request, type, id):

    if type == 'W':
        Calls = Call.objects.filter(worker_id = id)

    elif type == 'E':
        Calls = Call.objects.filter(employer_id = id)

    else:
        return HttpResponse(wrong_type, status= 400)

    return HttpResponse(json.dumps(list(Calls.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def get_all_applications (request, type, id):

    if type == 'W':
        Applications = Application.objects.filter(worker_id = id)

    elif type == 'J':
        Applications = Application.objects.filter(job_offer_id = id)

    else:
        return HttpResponse(wrong_type, status= 400)

    return HttpResponse(json.dumps(list(Applications.values()), indent = 4, default=str), content_type="application/json")

@require_http_methods(["GET"])
def search_Jobs (request):

    Offers = JobOffer.objects.all()

    return HttpResponse(json.dumps(list(Offers.values()), indent = 4, default=str), content_type="application/json")


#PUT
@require_http_methods(["PUT"])
def put_worker (request, oldName, oldPassword, name = None, password = None, birth_date = None, email = None, phone = None):
    id = get_id(oldName, oldPassword)

    if id == -1:
        return HttpResponse(wrong_id, status=401)

    worker = Worker.objects.get (pk = id)

    if name:
        worker.name = name

    if password:
        worker.password = password

    if birth_date is not None:
        if birth_date:
            worker.birth_date = birth_date
        else:
             worker.birth_date =  None

    if email is not None:
        if email:
            worker.email = email
        else:
             worker.email = None

    if phone is not None:
        if phone:
            worker.phone = phone
        else:
            worker.phone = None


    worker.save()
    return HttpResponse(succ_save + "Worker with id = " + str(id), status=200)

#def post_cv (request):
#doplnit ukladanie pdf
#worker.cv = ....

@require_http_methods(["PUT"])
def put_employer (request, oldName, oldPassword, name = None, password = None, birth_date = None, email = None, phone = None, companyId = None):
    id = get_id(oldName, oldPassword)

    if id == -1:
        return HttpResponse(wrong_id, status=401)

    employer = Employer.objects.get (pk = id)

    if name:
        employer.name = name

    if password:
        employer.password = password

    if birth_date is not None:
        if birth_date:
            employer.birth_date = birth_date
        else:
             employer.birth_date =  None

    if email is not None:
        if email:
            employer.email = email
        else:
             employer.email = None

    if phone is not None:
        if phone:
            employer.phone = phone
        else:
            employer.phone = None

    if companyId:
        company = Company.objects.get(pk = companyId)
        employer.company_id = company.id


    employer.save()
    return HttpResponse(succ_save + "Employer with id = " + str(id), status=200)

@require_http_methods(["PUT"])
def put_call (request, name, password, id, callName = None, status = None):
    userID = get_id(name, password)

    if userID == -1:
        return HttpResponse(wrong_id, status=401)

    call = Call.objects.get (pk = id)

    if userID != call.worker_id and userID != call.employer_id:      
        return HttpResponse(false_auth, status = 401)

    if name:
        call.name = callName

    if status:
        call.status = status

    call.save()
    return HttpResponse(succ_save + "Call with id = " + str(id), status=200)

@require_http_methods(["PUT"])
def put_job_offer (request, name, password, id, jobName = None, field = None, salary = None, working_hours = None, location = None, detail = None):
    employerID = get_id(name, password)

    if employerID == -1:
        return HttpResponse(wrong_id, status=401)
    
    offer = JobOffer.objects.get(pk = id)

    if employerID != offer.employer_id:
        return HttpResponse(false_auth, status = 401)

    if name:
        offer.name = jobName

    if field:
        offer.field = field

    if salary is not None:
        if salary:
            offer.salary = salary
        else:
            offer.salary = None

    if working_hours is not None:
        if working_hours:
            offer.working_hours = working_hours
        else:
            offer.working_hours = None

    if location is not None:
        if location:
            offer.location = location
        else:
            offer.location = None


    if detail is not None:
        if detail:
            offer.detail = detail
        else:
            offer.detail = None

    offer.save()
    return HttpResponse(succ_save + "Job offer with id = " + str(id), status=200)

@require_http_methods(["PUT"])
def put_applicationE (request, name, password, id, response):
    employerID = get_id(name, password)

    if employerID == -1:
        return HttpResponse(wrong_id, status=401)

    application = Application.objects.get(pk = id)
    offer = JobOffer.objects.get(pk = application.job_offer_id)

    if offer.employer_id != employerID:
        return HttpResponse(false_auth, status = 401)

    application.response = response

    application.save()
    return HttpResponse(succ_save + "Application with id = " + str(id), status=200)

@require_http_methods(["PUT"])
def put_applicationW (request , name, password, id , description = None, expires_on = None):
    workerID = get_id(name, password)

    if workerID == -1:
        return HttpResponse(wrong_id, status=401)
    
    application = Application.objects.get(pk = id)

    if application.worker_id != workerID:
        return HttpResponse(false_auth, status = 401)

    if description is not None:
        if description:
            application.description = description
        else:
            application.description = None

    if expires_on:
        application.expires_on = expires_on

    application.save()
    return HttpResponse(succ_save + "Application with id = " + str(id), status=200)


#POST
@require_http_methods(["POST"])
def post_worker (request, name, password, birth_date = None, email = None, phone = None): 
   query = Worker.objects.filter(name = name)

   if query:
       return HttpResponse(fail_create + "Worker with name = " + name, status=409)

   query = Employer.objects.filter(name = name)

   if query:
       return HttpResponse(fail_create + "Employer with name = " + name, status=409)

   newWorker = Worker(name=name, password=password)

   if birth_date:
       newWorker.birth_date = birth_date

   if email:
        newWorker.email = email
      
   if phone:
        newWorker.phone = phone
       
   newWorker.save()
   return HttpResponse(succ_create + "Worker with name = " + name, status=201)

@require_http_methods(["POST"])
def post_employer (request, name, password, companyName, birth_date = None, email = None, phone = None):
    query = Worker.objects.filter(name = name)

    if query:
       return HttpResponse(fail_create + "Worker with name = " + name, status=409)

    query = Employer.objects.filter(name = name)

    if query:
       return HttpResponse(fail_create + "Employer with name = " + name, status=409)

    query = Company.objects.filter(name = companyName)
            
    if not query: 
        return HttpResponse("Company with name = " + companyName + "does not exist", status=404)

    newEmployer = Employer(name=name, password=password, company_id=query[0].id)

    if birth_date:
        newEmployer.birth_date = birth_date

    if email:
        newEmployer.email = email
      
    if phone:
        newEmployer.phone = phone

    newEmployer.save()
    return HttpResponse(succ_create + "Employer with name = " + name, status=201)

@require_http_methods(["POST"])
def post_company (request, name, phone, email, website = None, detail = None):
    query = Company.objects.filter(name = name)
    
    if query: 
        return HttpResponse(fail_create + "Company with name = " + name, status=409)

    newCompany = Company(name = name,phone =  phone, email = email)

    if website:
       newCompany.website = website

    if detail:
        newCompany.detail = detail

    newCompany.save()
    return HttpResponse(succ_create + "Company with name = " + name , status=201)

@require_http_methods(["POST"])
def post_jobOffer (request, name, password,  job_name, field, salary = None, working_hours = None, location = None, detail = None):
    id = get_id(name, password)

    if id == -1:
        return HttpResponse(wrong_id, status=401)

    query = Employer.objects.filter(name = name, password = password)

    if not query:
        return HttpResponse("Only employer can create Job Offers", status=401)

    query = JobOffer.objects.filter(employer_id = id, name = job_name, field =field)

    if query:
        return HttpResponse(fail_create + "JobOffer with id = " + str(query[0].id), status=409)

    newOffer = JobOffer(name=job_name, employer_id=id, field=field)

    if salary:
        newOffer.salary=salary

    if working_hours:
        newOffer.working_hours=working_hours

    if location:
        newOffer.location=location

    if detail:
        newOffer.detail=detail
    
    newOffer.save()
    return HttpResponse(succ_create + "Job Offer with name = " + job_name, status=201)

@require_http_methods(["POST"])
def post_application (request, name, password, id, description = None, expires_on = None):
    workerID = get_id(name, password)

    if workerID == -1:
        return HttpResponse(wrong_id, status=401)

    query = Worker.objects.filter(name = name, password = password)

    if not query:
        return HttpResponse("Only worker can create Applications", status=401)

    query = Application.objects.filter(worker_id = workerID, job_offer_id = id)

    if query:
        return HttpResponse(fail_create + "Application with id = " + str(query[0].id), status=409)

    if not expires_on:
        expires_on = datetime.now() + timedelta(days=30)

    newApplication = Application(worker_id = workerID, job_offer_id = id, created_on = datetime.now(), expires_on =  expires_on)
    
    if description:
        newApplication.description = description
 
    newApplication.save()
    return HttpResponse(succ_create + "Application with worker_id = " + str(workerID) + " and job_offer_id = " + id, status=201)

@require_http_methods(["POST"])
def post_call (request,name, password, employer_id, worker_id, callName = None ):
    id = get_id(name, password)

    if id == -1 or (id != int(employer_id) and id != int(worker_id)):
        return HttpResponse(wrong_id, status=401)

    found = None

    job = JobOffer.objects.filter(employer_id = employer_id)

    for j in job:
        query = Application.objects.filter(worker_id = worker_id, job_offer_id = j.id, response = True)
        if query:
            found = j.name

    if not found:
        return HttpResponse("Cannot create call, Accepted application doesnt exist!", status=404)

    if not callName:
        callName = found + " - Call"

    newCall = Call(employer_id = employer_id, worker_id = worker_id, name = callName, status = False)

    newCall.save()
    return HttpResponse(succ_create + "Call with name = " + callName, status=201)


#DELETE
@require_http_methods(["DELETE"])
def delete_user (request, type, name, password):

    user_id = get_id(name, password)

    if user_id == -1 :
        return HttpResponse(wrong_id, status=401)

    if type == 'W':         
        Application.objects.filter(worker_id=user_id).delete() 
        Call.objects.filter(worker_id=user_id).delete()
        Worker.objects.filter(id=user_id).delete() 

    elif type == 'E':         
        query = JobOffer.objects.raw('SELECT id FROM job_offer WHERE employer_id =' + str(user_id) + ';') #zistenie idciek JobOffer-ov vytvorenych danym employer-om
        for vysledok in query:
            Application.objects.filter(job_offer_id=vysledok.id).delete()

        JobOffer.objects.filter(employer_id=user_id).delete() 
        Call.objects.filter(employer_id=user_id).delete()
        Employer.objects.filter(id=user_id).delete()

    else:
        return HttpResponse(wrong_type, status=400)
 
    return HttpResponse(succ_delete + "User with id = " + str(user_id), status=200)

@require_http_methods(["DELETE"])
def delete_jobOffer (request,name, password, id):
    user_id = get_id(name, password)

    if user_id == -1:
        return HttpResponse(wrong_id, status=401)

    job = JobOffer.objects.get(pk = id)

    if job.employer_id != user_id:
        return HttpResponse(false_auth, status = 401)


    Application.objects.filter(job_offer_id=id).delete() 
    JobOffer.objects.filter(id=id).delete()

    return HttpResponse(succ_delete + "Job offer with id = " + str(id), status=200)

def delete_application (request, name, password, id):
    user_id = get_id(name, password)

    if user_id == -1:
        return HttpResponse(wrong_id, status=401)

    app = Application.objects.get(pk = id)

    if app.worker_id != user_id:
        return HttpResponse(false_auth, status = 401)


    Application.objects.filter(id=id).delete()

    return HttpResponse(succ_delete + "Application with id = " + str(id), status=200)
