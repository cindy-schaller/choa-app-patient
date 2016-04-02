from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from fhirclient import client
from fhirclient.models import patient, questionnaire, questionnaireresponse

from datetime import datetime

# Create views here.
def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def respond(request):
    settings = {
        'app_id': 'omscs-hit-cdc',
        'api_base': 'http://52.72.172.54:8080/fhir/baseDstu2'
    }
    smart = client.FHIRClient(settings=settings)
    patientId = request.COOKIES.get('userId')
    #childRecord = patient.Patient.read('18907426', smart.server)
    childRecord = patient.Patient.read(patientId, smart.server)
    #smart.human_name(childRecord.name[0])
    age = (datetime.now().date() - childRecord.birthDate.date).days / 365.24

    form = questionnaire.Questionnaire.read("18791835", smart.server)
    if age < 13:
        form = questionnaire.Questionnaire.read("18791830", smart.server)

    context = RequestContext(request)
    context['patientName'] = smart.human_name(childRecord.name[0])
    context['questionnaire'] = form.group.question

    return render_to_response('questionnaire.html',
                              context_instance=context)

def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
