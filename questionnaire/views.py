from django.shortcuts import render,render_to_response,redirect
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from fhirclient import client
from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from datetime import datetime
from importlib import import_module

# Create views here.
from fhirclient.server import FHIRNotFoundException


def getFhirConnectionInfo():
    return {
        'app_id': 'omscs-hit-cdc',
        'api_base': 'http://52.72.172.54:8080/fhir/baseDstu2'
    }


def getFhirClient():
    return client.FHIRClient(settings=getFhirConnectionInfo())


def resolveFhirReference(fhir_reference, server):
    permitted_modules = {"Patient": "patient", "Practitioner": "practitioner", "Questionnaire": "questionnaire"}
    klassname, ref_id = fhir_reference.reference.rsplit('/', 1)
    if klassname in permitted_modules:
        module = import_module("fhirclient.models."+permitted_modules[klassname])
        klass = getattr(module, klassname)
        return klass.read(ref_id, server)
    else:
        raise FHIRNotFoundException("Unsupported class "+klassname+" in reference "+fhir_reference.reference)

def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))

def respond(request):
    smart = getFhirClient()
    patientId = request.COOKIES.get('userId')
    if patientId:
        try:
            childRecord = patient.Patient.read(patientId, smart.server)
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
                return redirect("/questionnaire/")

            context = RequestContext(request)
            context['patientName'] = smart.human_name(childRecord.name[0])
            context['questionnaire'] = form.group.question
            context['json'] = jsonResponse

            #return JsonResponse(jsonResponse)
            return render_to_response('questionnaire.html',
                                      context_instance=context)
        except Exception:
            return HttpResponse("The user you've selected appears to be invalid.  Please return to <a href='/questionnaire/'>the index</a> and select a different user.")
    else:
        return redirect("questionnaire.views.index")


def messages(request):
    smart = getFhirClient()
    patientId = request.COOKIES.get('userId')

    try:
        search = communication.Communication.where(struct={"recipient": "Patient/"+patientId})
        messages = search.perform(smart.server)
        if messages.total > 0:
            context = RequestContext(request)
            context['messages'] = map(lambda(entry): entry.resource, messages.entry)
            return render_to_response('messages.html',
                                      context_instance=context)
        else:
            return HttpResponse("No messages yet.  Check back soon!")

    except Exception:
        return HttpResponse("The user you've selected appears to be invalid.  Please return to <a href='/questionnaire/'>the index</a> and select a different user.")


def history(request):
    smart = getFhirClient()
    patientId = request.COOKIES.get('userId')

    try:
        search = questionnaireresponse.QuestionnaireResponse.where(struct={"patient": patientId})
        responses = search.perform(smart.server)
        if responses.total > 0:
            context = RequestContext(request)
            context['pastResponses'] = map(lambda(entry): entry.resource, responses.entry)
            return render_to_response('history.html',
                                      context_instance=context)
        else:
            return redirect("questionnaire.views.respond")
    except FHIRNotFoundException:
        return HttpResponse("The user you've selected appears to be invalid.  Please return to <a href='/questionnaire/'>the index</a> and select a different user.")


def details(request, responseid):
    smart = getFhirClient()
    patientId = request.COOKIES.get('userId')

    try:
        response = questionnaireresponse.QuestionnaireResponse.read(responseid, smart.server)
        questionnaire = resolveFhirReference(response.questionnaire, server=smart.server)
        context = RequestContext(request)
        context['response'] = response
        context['questionnaire'] = questionnaire
        return render_to_response('response-details.html',
                                  context_instance=context)
    except FHIRNotFoundException:
        return HttpResponse("The response you've selected appears to be invalid.  Please return to <a href='/questionnaire/history'>the index</a> and select another.")


def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
