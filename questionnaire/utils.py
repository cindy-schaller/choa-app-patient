from fhirclient import client
from fhirclient.server import FHIRNotFoundException
from importlib import import_module

MIHIN = 'MiHIN'
SMART = 'SMART'
TEEN_FORM = 'questionnaire-healthy-habits-adolescent'
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
            '11034584': 'Parent/guardian of Clark, age 5'
        }
    }


def getQuestionnaireMap():
    return {
        MIHIN: {
            TEEN_FORM: '11034668',
            CHILD_FORM: '11034671'
        },
        SMART: {
            TEEN_FORM: '572357f90cf20e9addb2a71a',
            CHILD_FORM: '572358140cf20e9addb2a71b'
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
