from django.core.management.base import BaseCommand
from fhirclient.models import patient, questionnaire, questionnaireresponse, organization
from questionnaire import utils
'''
displays the reference id's conveiently as follows from terminal:
    manage.py dump_resources MiHIN
can use this file to create the reference include as follows
    manage.py dump_resources MiHIN>json_data/tools/db_references.py
'''

class Command(BaseCommand):
    args = '{MiHIN, SMART}'
    help = 'Conveniently get ids of existing resources.'

    def add_arguments(self, parser):
        parser.add_argument('server-id', nargs=1)

    def handle(self, *args, **options):
        client = utils.getFhirClient(options['server-id'][0])
        server = client.server

        # resource type, /search criteria, print name
        data = [
            ("Patient", {"family": "Kent", "given": "Clark"}, "REF_CLARK = "),
            ("Patient", {"family": "Kent", "given": "Kara"}, "REF_KARA = "),
            ("Patient", {"family": "Prince", "given": "Diana"}, "REF_DIANA_PRINCE = "),
            ("Patient", {"family": "Prior", "given": "Beatrice"}, "REF_BEATRICE_PRIOR = "),
            ("Patient", {"family": "Eaton", "given": "Tobias"}, "REF_TOBIAS_EATON = "),
            ("Questionnaire", {"title": "Healthy Habits Tracker (adolescent)"}, "REF_HHA_TEEN = "),
            ("Questionnaire", {"title": "Healthy Habits Questionnaire"}, "REF_HHA_CHILD = "),
            ("Questionnaire", {"title": "WIC Child Nutrition Questionnaire"}, "REF_WIC = "),
            ("Questionnaire", {"title": "Healthy Habits Goal Questionnaire"}, "REF_GOALS = "),
            ("Questionnaire", {"title": "Healthy Habits Goal Status"}, "REF_STATUS = "),
            ("Questionnaire", {"title": "Food Insecurity Questionnaire"}, "REF_INSECURITY = "),
            ("Organization", {"name": "WIC"}, "REF_WIC_ORG = "),
            ("Organization", {"name": "MD"}, "REF_MD_ORG = "),
            ("Organization", {"name": "Patient Care Coordinator"}, "REF_PATCO_ORG = "),
        ]

        for item in data:
            valid_entry = True
            r_type, criteria, output = item
            if r_type == "Patient":
                search = patient.Patient.where(struct=criteria)
            elif r_type == "Questionnaire":
                search = questionnaire.Questionnaire.where(struct=criteria)
            elif r_type == "Organization":
                search = organization.Organization.where(struct=criteria)
            else:
                valid_entry = False
                print "Invalid entry in lookup list"

            if valid_entry:
                resources = search.perform(server)
                if resources.total > 0:
                    for entry in resources.entry:
                        print output + "'" + entry.resource.id +"'"
                else: print output + ": not found"

