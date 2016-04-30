import pytz as pytz

from functools import wraps

from django.utils import timezone
from django.utils.decorators import available_attrs
from django.core.urlresolvers import reverse

from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from datetime import datetime

import utils


def require_valid_user(view_func, invalid_user_message=None):
    if invalid_user_message is None:
        invalid_user_message = "The user you've selected appears to be invalid. \
         Please return to <a href='/questionnaire/'>the index</a> and select a different user."
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped(request, *args, **kwargs):
        if request.COOKIES.get('userId') is not None:
            try:
                (patientId, serverId) = get_login_info(request)
                smart = utils.getFhirClient(serverId)
                patient.Patient.read(patientId, smart.server)
            except Exception:
                context = RequestContext(request)
                context['error_text'] = invalid_user_message
                return render_to_response('error.html',
                                      context_instance=context)
            return view_func(request, *args, **kwargs)
        else:
            return redirect("questionnaire.views.index")
    return _wrapped


def get_login_info(request):
    patientId = request.COOKIES.get('userId')
    serverId = utils.resolveServerId(patientId,request.COOKIES.get('serverId'))
    return (patientId, serverId)


def index(request):
    context = RequestContext(request)
    context['patientGroups'] = utils.getPatientMap()
    return render_to_response('index.html',
                              context_instance=context)


@require_valid_user
def respond(request):
    (patientId, serverId) = get_login_info(request)
    smart = utils.getFhirClient(serverId)

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


@require_valid_user
def messages(request):
    timezone.activate(pytz.timezone("US/Eastern"))
    (patientId, serverId) = get_login_info(request)
    smart = utils.getFhirClient(serverId)

    search = communication.Communication.where(struct={"recipient": "Patient/"+patientId})
    # This is a hack to work around a bug in the SMART on FHIR server.
    # The bug should go away when they finish their switch to a HAPI FHIR-based implementation.
    if serverId == utils.SMART:
        search = communication.Communication.where(struct={"recipient": patientId})
    messages = search.perform_resources(smart.server)
    if len(messages) > 0:
        context = RequestContext(request)

        def timestamp_key(entry):
            return entry.sent.date

        context['messages'] = sorted(messages, key=timestamp_key, reverse=True)
        return render_to_response('messages.html',
                                  context_instance=context)
    else:
        context = RequestContext(request)
        context['error_text'] = "No messages yet.  Check back soon!"
        return render_to_response('error.html',
                                  context_instance=context)


@require_valid_user
def history(request):
    timezone.activate(pytz.timezone("US/Eastern"))
    (patientId, serverId) = get_login_info(request)
    smart = utils.getFhirClient(serverId)

    search = questionnaireresponse.QuestionnaireResponse.where(struct={"patient": patientId})
    responses = search.perform_resources(smart.server)
    if len(responses) > 0:
        context = RequestContext(request)

        def timestamp_key(entry):
            return entry.meta.lastUpdated.date

        context['pastResponses'] = sorted(responses, key=timestamp_key, reverse=True)
        return render_to_response('history.html',
                                  context_instance=context)
    else:
        context = RequestContext(request)
        context['error_text'] = "You don't have any history yet. \
         <a href='"+reverse("questionnaire.views.respond")+"'>Fill out the questionnaire</a> to get started!"
        return render_to_response('error.html',
                                  context_instance=context)


@require_valid_user
def details(request, responseid):
    timezone.activate(pytz.timezone("US/Eastern"))
    (patientId, serverId) = get_login_info(request)
    smart = utils.getFhirClient(serverId)

    try:
        response = questionnaireresponse.QuestionnaireResponse.read(responseid, smart.server)
        questionnaire = utils.resolveFhirReference(response.questionnaire, server=smart.server)
        context = RequestContext(request)
        context['response'] = response
        context['questionnaire'] = questionnaire
        return render_to_response('response-details.html',
                                  context_instance=context)
    except Exception:
        context = RequestContext(request)
        context['error_text'] = "The response you've selected appears to be invalid. \
         Please return to <a href='/questionnaire/history'>the index</a> and select another."
        return render_to_response('error.html',
                                  context_instance=context)


def about(request):
    return render_to_response('about.html',
                              context_instance=RequestContext(request))
