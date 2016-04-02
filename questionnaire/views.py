from django.shortcuts import render,render_to_response
from django.http import HttpResponse, JsonResponse
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

    jsonResponse = []
    if request.method == 'POST':
        jsonResponse = {"group": {"linkId": "root", "question": []}, "resourceType": "QuestionnaireResponse",
                        "questionnaire": {"reference": "Questionnaire/"+form.id}, "status": "completed",
                        "subject": {"reference": "Patient/"+childRecord.id},
                        "author": {"reference": "Patient/"+childRecord.id}}
        for question in form.group.question:
            questionJson = {"linkId": question.linkId, "answer": [{"valueInteger": request.POST[question.linkId]}]}
            jsonResponse["group"]["question"].append(questionJson)
        smart.server.post_json('QuestionnaireResponse', jsonResponse)
        #response = questionnaireresponse.QuestionnaireResponse()
        #response.group = questionnaireresponse.QuestionnaireResponseGroup()
        #for questionId in request.POST.keys:
        #    question = questionnaireresponse.QuestionnaireResponseGroupQuestion()
        #    question.linkId = questionId
        #    question.answer = questionnaireresponse.QuestionnaireResponseGroupQuestionAnswer()
        #    question.answer.valueString = request.POST[questionId]
        #    response.group.question.add(question)

    context = RequestContext(request)
    context['patientName'] = smart.human_name(childRecord.name[0])
    context['questionnaire'] = form.group.question
    context['json'] = jsonResponse

    #return JsonResponse(jsonResponse)
    return render_to_response('questionnaire.html',
                              context_instance=context)

def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
