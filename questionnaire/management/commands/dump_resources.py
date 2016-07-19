from django.core.management.base import BaseCommand
from fhirclient.models import patient, questionnaire, questionnaireresponse, organization
from questionnaire import utils


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
            ("Patient", {"family": "Kent", "given": "Clark"}, "Clark Kent"),
            ("Patient", {"family": "Kent", "given": "Kara"}, "Kara Kent"),
            ("Patient", {"family": "Prince", "given": "Diana"}, "Diana Prince"),
            ("Patient", {"family": "Prior", "given": "Beatrice"}, "Beatrice Prior"),
            ("Patient", {"family": "Eaton", "given": "Tobias"}, "Tobias Eaton"),
            ("Questionnaire", {"title": "Healthy Habits Tracker (adolescent)"}, "Adolescent questionnaire"),
            ("Questionnaire", {"title": "Healthy Habits Questionnaire"}, "Child questionnaire"),
            ("Questionnaire", {"title": "WIC Child Nutrition Questionnaire"}, "WIC questionnaire"),
            ("Questionnaire", {"title": "Healthy Habits Goal Questionnaire"}, "Goals questionnaire"),
            ("Questionnaire", {"title": "Healthy Habits Goal Status"}, "Goal Status questionnaire"),
            ("Questionnaire", {"title": "Food Insecurity Questionnaire"}, "Food Insecurity questionnaire"),
            ("Organization", {"name": "WIC"}, "WIC organization"),
            ("Organization", {"name": "MD"}, "MD organization"),
            ("Organization", {"name": "Patient Care Coordinator"}, "Patient Care Coordinator organization"),
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
                        print output + ": " + entry.resource.id
                else: print output + ": not found"

