from django.shortcuts import render,render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from fhirclient import client
from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from datetime import datetime
from importlib import import_module

# Create views here.
from fhirclient.server import FHIRNotFoundException


MIHIN = 'MiHIN'
SMART = 'SMART'
TEEN_FORM = 'questionnaire-healthy-habits-teen'
CHILD_FORM = 'questionnaire-healthy-habits-child'


def getFhirConnectionInfo(serverId):
    serverMap = {
        MIHIN: {
            'app_id': 'omscs-hit-cdc',
            'api_base': 'http://52.72.172.54:8080/fhir/baseDstu2'
        },
        SMART: {
            'app_id': 'omscs-hit-cdc',
            'api_base': 'https://fhir-open-api-dstu2.smarthealthit.org/'
        }
    }
    return serverMap[serverId]


def getPatientMap():
    return {
        MIHIN: {
            '18791941': 'Parent/guardian of Clark, age 10',
            '18791962': 'Parent/guardian of Diana, age 8',
            '18791983': 'Beatrice, age 14',
            '18792004': 'Tobias, age 15'
        },
        SMART: {
            '571ada5e0cf20e9addb27239': 'Parent/guardian of Clark, age 10',
            '571ada5e0cf20e9addb2723a': 'Parent/guardian of Diana, age 8',
            '571ada5d0cf20e9addb27238': 'Beatrice, age 14',
            '571ada5e0cf20e9addb2723b': 'Tobias, age 15'
        }
    }


def getQuestionnaireMap():
    return {
        MIHIN: {
            TEEN_FORM: '18791835',
            CHILD_FORM: '18791830'
        },
        SMART: {
            TEEN_FORM: '571adc040cf20e9addb27240',
            CHILD_FORM: '571adc030cf20e9addb2723f'
        }
    }


def resolveServerId(patientId, serverId):
    # Allowing this kind of fallback is a little dubious, since in principle nothing prevents the same patient ID
    # from occurring on two separate servers.  But it makes life a little more convenient for people who are already
    # logged in, so we'll allow it.
    patientMap = getPatientMap()
    if serverId is None:
        for key in patientMap.keys():
            if patientId in patientMap[key].keys():
                serverId = key
    return serverId


def getFhirClient(serverId):
    return client.FHIRClient(settings=getFhirConnectionInfo(serverId))


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
    context = RequestContext(request)
    context['patientGroups'] = getPatientMap()
    return render_to_response('index.html',
                              context_instance=context)


def respond(request):
    patientId = request.COOKIES.get('userId')
    serverId = resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = getFhirClient(serverId)
    if patientId:
        try:
            childRecord = patient.Patient.read(patientId, smart.server)
            age = (datetime.now().date() - childRecord.birthDate.date).days / 365.24

            qMap = getQuestionnaireMap()
            form = questionnaire.Questionnaire.read(qMap[serverId][TEEN_FORM], smart.server)
            if age < 13:
                    form = questionnaire.Questionnaire.read(qMap[serverId][CHILD_FORM], smart.server)

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
    serverId = resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = getFhirClient(serverId)

    try:
        search = communication.Communication.where(struct={"recipient": "Patient/"+patientId})
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
    serverId = resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = getFhirClient(serverId)

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
    serverId = resolveServerId(patientId,request.COOKIES.get('serverId'))
    smart = getFhirClient(serverId)

    try:
        response = questionnaireresponse.QuestionnaireResponse.read(responseid, smart.server)
        questionnaire = resolveFhirReference(response.questionnaire, server=smart.server)
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
