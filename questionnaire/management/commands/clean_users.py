import json

from django.core.management.base import BaseCommand

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from questionnaire import utils


class Command(BaseCommand):
    args = '{MiHIN, SMART}'
    help = 'Delete all questionnaire responses and messages for a user.'

    def add_arguments(self, parser):
        parser.add_argument('server-id', nargs=1)

    def handle(self, *args, **options):
        server_id = options['server-id'][0]
        client = utils.getFhirClient(server_id)
        server = client.server
        for patient in utils.getPatientMap()[server_id].keys():
            search = questionnaireresponse.QuestionnaireResponse.where(struct={"patient": patient})
            responses = search.perform(server)
            if responses.total > 0:
                for entry in responses.entry:
                    entry.resource.delete()
                    print "Deleted: "+entry.resource.as_json()
            search = communication.Communication.where(struct={"recipient": patient})
            communications = search.perform(server)
            if communications.total > 0:
                for entry in communications.entry:
                    entry.resource.delete()
                    print "Deleted: "+entry.resource.as_json()