import json
from importlib import import_module

from django.core.management.base import BaseCommand

from fhirclient.models import patient, questionnaire, questionnaireresponse, communication, practitioner

from questionnaire import utils


class Command(BaseCommand):
    args = '{MiHIN, SMART} <resource-type> <resource-id> <json-path>'
    help = 'Update a particular FHIR resource with the latest reference JSON.'

    def add_arguments(self, parser):
        parser.add_argument('server-id',)
        parser.add_argument('resource-type')
        parser.add_argument('resource-id')
        parser.add_argument('json-path')

    def handle(self, *args, **options):
        client = utils.getFhirClient(options['server-id'])
        server = client.server
        type = options['resource-type']
        id = options['resource-id']
        path = options['json-path']

        with open('json_data/'+path, 'r') as h:
            raw_json = json.load(h)
            if "id" in raw_json:
                del raw_json["id"]
            try:
                klassname = type
                module = import_module("fhirclient.models."+klassname.lower())
                klass = getattr(module, klassname)
                existing = klass.read(id, server)

                server.put_json(type+"/"+id, raw_json)
            except Exception as e:
                print e
                print "Warning: "+type+"/"+id+" does not exist, creating"

                server.post_json(type, raw_json)