import json

from django.core.management.base import BaseCommand

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner, organization

from questionnaire import utils


class Command(BaseCommand):
    args = '{MiHIN, SMART} [--include-patients] [--include-questionnaires] [--include-organizations]'
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
        parser.add_argument('include-organizations',
            action='store_true',
            default=False,
            help='Include organizations? (defaults to no)')


    def handle(self, *args, **options):
        client = utils.getFhirClient(options['server-id'])
        server = client.server
        include_patients = options['include-patients']
        include_questionnaires = options['include-questionnaires']
        include_organizations = options['include-organizations']

        if include_patients:
            patients = ['patient1.json', 'patient2.json', 'patient3.json', 'patient4.json', 'patient5.json']
            for filename in patients:
                with open('json_data/'+filename, 'r') as h:
                    pjson = json.load(h)
                    identifier = pjson["identifier"][0]["value"]
                    name = " ".join(map(lambda x: x[0], pjson["name"][0].values()))
                    print name

                    search = patient.Patient.where(struct={"identifier": identifier})
                    existing = search.perform(server)
                    if existing.total > 0:
                        for entry in existing.entry:
                            print "Warning - patient " + name + " already exists as ID " + entry.resource.id + ", attempting update"
                            server.put_json('Patient/'+entry.resource.id, pjson)
                    else:
                        response = server.post_json('Patient', pjson)
                        print response
        if include_questionnaires:
            questionnaires = ['questionnaire-adolescent.json', 'questionnaire-child.json',
                              'questionnaire-food-insecurity.json', 'questionnaire-wic-child-nutrition.json',
                              'questionnaire-healthy-habit-goals.json','questionnaire-healthy-habit-goal-status.json']
            for filename in questionnaires:
                with open('json_data/'+filename, 'r') as h:
                    qjson = json.load(h)
                    name = qjson["group"]["title"]
                    print name

                    search = questionnaire.Questionnaire.where(struct={"title": name})
                    existing = search.perform(server)
                    if existing.total > 0:
                        for entry in existing.entry:
                            print "Warning - questionnaire " + name + " already exists as ID " + entry.resource.id + ", attempting update"
                            server.put_json('Questionnaire/'+entry.resource.id, qjson)
                    else:
                        response = server.post_json('Questionnaire', qjson)
                        print response

        if include_organizations:
            organizations = ['organization-md.json', 'organization-patco.json', 'organization-wic.json']
            for filename in organizations:
                with open('json_data/'+filename, 'r') as h:
                    ojson = json.load(h)
                    name = ojson["name"]
                    print name

                    search = organization.Organization.where(struct={"name": name})
                    existing = search.perform(server)
                    if existing.total > 0:
                        for entry in existing.entry:
                            print "Warning - organization " + name + " already exists as ID " + entry.resource.id + ", attempting update"
                            server.put_json('Organization/'+entry.resource.id, ojson)
                    else:
                        response = server.post_json('Organization', ojson)
                        print response

        for message in ['message1.json']:
           with open('json_data/'+message, 'r') as h:
                mjson = json.load(h)
                #server.post_json('Communication', mjson)