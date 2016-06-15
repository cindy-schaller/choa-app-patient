import json

from django.core.management.base import BaseCommand

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from questionnaire import utils


class Command(BaseCommand):
    args = '{MiHIN, SMART} [--include-patients] [--include-questionnaires]'
    help = 'Load resources into a FHIR server from the reference JSON.'

    def add_arguments(self, parser):
        parser.add_argument('server-id')
        parser.add_argument('include-patients',
            action='store_true',
            default=False,
            help='Include patients? (defaults to no)')
        parser.add_argument('include-questionnaires',
            action='store_true',
            default=False,
            help='Include questionnaires? (defaults to no)')

    def handle(self, *args, **options):
        client = utils.getFhirClient(options['server-id'])
        server = client.server
        include_patients = options['include-patients']
        include_questionnaires = options['include-questionnaires']

        if include_patients:
            patients = ['patient1.json', 'patient2.json', 'patient3.json', 'patient4.json']
            for filename in patients:
                with open('json_data/'+filename, 'r') as h:
                    pjson = json.load(h)
                    name = " ".join(map(lambda x: x[0], pjson["name"][0].values()))
                    print name

                    search = patient.Patient.where(struct={"name": name})
                    existing = search.perform(server)
                    if existing.total > 0:
                        print "Warning - patient "+name+" already exists, attempting update"
                        for entry in existing.entry:
                            server.put_json('Patient/'+entry.id, pjson)
                    else:
                        response = server.post_json('Patient', pjson)
                        print response
        if include_questionnaires:
            questionnaires = ['questionnaire-adolescent.json', 'questionnaire-child.json']
            for filename in questionnaires:
                with open('json_data/'+filename, 'r') as h:
                    qjson = json.load(h)
                    name = qjson["group"]["title"]

                    search = questionnaire.Questionnaire.where(struct={"title": name})
                    existing = search.perform(server)
                    if existing.total > 0:
                        print "Warning - questionnaire "+name+" already exists, attempting update"
                        for entry in existing.entry:
                            server.put_json('Questionnaire/'+entry.id, qjson)
                    else:
                        response = server.post_json('Questionnaire', qjson)
                        print response
        for message in ['message1.json']:
           with open('json_data/'+message, 'r') as h:
                mjson = json.load(h)
                #server.post_json('Communication', mjson)