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
            '18791941': 'Parent/guardian of Clark, age 10',
            '18791962': 'Parent/guardian of Diana, age 8',
            '18791983': 'Beatrice, age 14',
            '18792004': 'Tobias, age 15'
        },
        SMART: {
            '5722014c0cf20e9addb273be': 'Parent/guardian of Clark, age 10',
            '5722014c0cf20e9addb273bf': 'Parent/guardian of Diana, age 8',
            '5722014b0cf20e9addb273bd': 'Beatrice, age 14',
            '5722014c0cf20e9addb273c0': 'Tobias, age 15'
        }
    }


def getQuestionnaireMap():
    return {
        MIHIN: {
            TEEN_FORM: '18791835',
            CHILD_FORM: '18791830'
        },
        SMART: {
            TEEN_FORM: '5722008e0cf20e9addb273bb',
            CHILD_FORM: '5722008e0cf20e9addb273ba'
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
