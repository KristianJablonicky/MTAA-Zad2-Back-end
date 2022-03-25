"""
Definition of views.
"""
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict

from datetime import datetime
import json
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
