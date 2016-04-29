from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import json

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from datetime import datetime
from importlib import import_module

# Create views here.
from fhirclient.server import FHIRNotFoundException

import utils


def index(request):
    context = RequestContext(request)
    context['patientGroups'] = utils.getPatientMap()
    return render_to_response('index.html',
                              context_instance=context)


def respond(request):
    patientId = request.COOKIES.get('userId')
    serverId = utils.resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = utils.getFhirClient(serverId)
    if patientId:
        try:
            childRecord = patient.Patient.read(patientId, smart.server)
            age = (datetime.now().date() - childRecord.birthDate.date).days / 365.24

            qMap = utils.getQuestionnaireMap()
            form = questionnaire.Questionnaire.read(qMap[serverId][utils.TEEN_FORM], smart.server)
            if age < 13:
                    form = questionnaire.Questionnaire.read(qMap[serverId][utils.CHILD_FORM], smart.server)

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
            context = RequestContext(request)
            context['error_text'] = "The user you've selected appears to be invalid. \
             Please return to <a href='/questionnaire/'>the index</a> and select a different user."
            return render_to_response('error.html',
                                      context_instance=context)
    else:
        return redirect("questionnaire.views.index")


def messages(request):
    patientId = request.COOKIES.get('userId')
    serverId = utils.resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = utils.getFhirClient(serverId)

    try:
        search = communication.Communication.where(struct={"recipient": "Patient/"+patientId})
        # This is a hack to work around a bug in the SMART on FHIR server.
        # The bug should go away when they finish their switch to a HAPI FHIR-based implementation.
        if serverId == utils.SMART:
            search = communication.Communication.where(struct={"recipient": patientId})
        messages = search.perform(smart.server)
        if messages.total > 0:
            context = RequestContext(request)
            context['messages'] = map(lambda(entry): entry.resource, messages.entry)
            return render_to_response('messages.html',
                                      context_instance=context)
        else:
            context = RequestContext(request)
            context['error_text'] = "No messages yet.  Check back soon!"
            return render_to_response('error.html',
                                      context_instance=context)

    except Exception:
        context = RequestContext(request)
        context['error_text'] = "The user you've selected appears to be invalid. \
         Please return to <a href='/questionnaire/'>the index</a> and select a different user."
        return render_to_response('error.html',
                                  context_instance=context)


def history(request):
    patientId = request.COOKIES.get('userId')
    serverId = utils.resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = utils.getFhirClient(serverId)

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
    except Exception:
        context = RequestContext(request)
        context['error_text'] = "The user you've selected appears to be invalid. \
         Please return to <a href='/questionnaire/'>the index</a> and select a different user."
        return render_to_response('error.html',
                                  context_instance=context)


def details(request, responseid):
    patientId = request.COOKIES.get('userId')
    serverId = utils.resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = utils.getFhirClient(serverId)

    try:
        response = questionnaireresponse.QuestionnaireResponse.read(responseid, smart.server)
        questionnaire = utils.resolveFhirReference(response.questionnaire, server=smart.server)
        context = RequestContext(request)
        context['response'] = response
        context['questionnaire'] = questionnaire
        return render_to_response('response-details.html',
                                  context_instance=context)
    except FHIRNotFoundException:
        context = RequestContext(request)
        context['error_text'] = "The response you've selected appears to be invalid. \
         Please return to <a href='/questionnaire/history'>the index</a> and select another."
        return render_to_response('error.html',
                                  context_instance=context)


def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
