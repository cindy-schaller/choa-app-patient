from django.core.management.base import BaseCommand

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from questionnaire import utils

patients = ['patient1.json', 'patient2.json', 'patient3.json', 'patient4.json', 'patient5.json']


class Command(BaseCommand):
    args = '{MiHIN, SMART}'
    help = 'Conveniently get ids of existing resources.'

    def add_arguments(self, parser):
        parser.add_argument('server-id', nargs=1)

    def handle(self, *args, **options):
        client = utils.getFhirClient(options['server-id'][0])
        server = client.server

        search = patient.Patient.where(struct={"name": "Kent"})
        patients = search.perform(server)
        for entry in patients.entry:
            print "Clark Kent: " + entry.resource.id
        search = patient.Patient.where(struct={"name": "Prince"})
        patients = search.perform(server)
        for entry in patients.entry:
            print "Diana Prince: " + entry.resource.id
        search = patient.Patient.where(struct={"name": "Prior"})
        patients = search.perform(server)
        for entry in patients.entry:
            print "Beatrice Prior: " + entry.resource.id
        search = patient.Patient.where(struct={"name": "Eaton"})
        patients = search.perform(server)
        for entry in patients.entry:
            print "Tobias Eaton: " + entry.resource.id

        print ""
        search = questionnaire.Questionnaire.where(struct={"title": "Health Habits Tracker (adolescent)"})
        questionnaires = search.perform(server)
        for entry in questionnaires.entry:
            print "Adolescent questionnaire: " + entry.resource.id

        search = questionnaire.Questionnaire.where(struct={"title": "Healthy Habits Questionnaire"})
        questionnaires = search.perform(server)
        for entry in questionnaires.entry:
            print "Child questionnaire: " + entry.resource.id