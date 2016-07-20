from django.core.management.base import BaseCommand
import json_data.tools.gen_boy_obs
import json_data.tools.gen_girl_obs
import json_data.tools.generate_qresponse_food_insecurity
import json_data.tools.generate_qresponse_HHA
import json_data.load_files_to_MiHIN

'''
this is a batch command that consolidates generators and loaders
that are dependent on reference from patients and questionnaires
run this after recreating the references for patients and questionnaires
'''

class Command(BaseCommand):
    args = '{MiHIN, SMART} [--include-patients] [--include-questionnaires] [--include-organizations]'
    help = 'Load resources into a FHIR server from the reference JSON.'

    def add_arguments(self, parser):
        parser.add_argument('server-id')

    def handle(self, *args, **options):
        json_data.tools.gen_boy_obs.main()
        json_data.tools.gen_girl_obs.main()
        json_data.tools.generate_qresponse_food_insecurity.main()
        json_data.tools.generate_qresponse_HHA.main()
        json_data.load_files_to_MiHIN.main()
