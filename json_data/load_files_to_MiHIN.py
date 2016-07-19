# basic method to load to MiHIN
# should make nicer and add to loaders in django management
import os
import json
import questionnaire.utils

obs_dir_kara = 'ob-kara'
obs_files_kara = ['ob-kara-ht-0.json', 'ob-kara-ht-1.json', 'ob-kara-ht-2.json',
                  'ob-kara-ht-3.json', 'ob-kara-ht-4.json', 'ob-kara-ht-5.json',
                  'ob-kara-ht-6.json', 'ob-kara-ht-7.json', 'ob-kara-ht-8.json',
                  'ob-kara-ht-9.json', 'ob-kara-wt-0.json', 'ob-kara-wt-1.json',
                  'ob-kara-wt-2.json', 'ob-kara-wt-3.json', 'ob-kara-wt-4.json',
                  'ob-kara-wt-5.json', 'ob-kara-wt-6.json', 'ob-kara-wt-7.json',
                  'ob-kara-wt-8.json', 'ob-kara-wt-9.json']
fam_hist_files_kara = ['ob-kara-mth.json', 'ob-kara-fth.json']
rel_person_files_kara = ['rp-kara-mth.json', 'rp-kara-sib.json']

obs_dir_clark = 'ob-clark'
obs_files_clark = [
    'ob-clark-ht-0.json', 'ob-clark-ht-1.json', 'ob-clark-ht-2.json',
    'ob-clark-ht-3.json', 'ob-clark-ht-4.json', 'ob-clark-ht-5.json',
    'ob-clark-ht-6.json', 'ob-clark-ht-7.json', 'ob-clark-ht-8.json',
    'ob-clark-ht-9.json', 'ob-clark-ht-9.json', 'ob-clark-ht-10.json',
    'ob-clark-wt-0.json', 'ob-clark-wt-1.json',
    'ob-clark-wt-2.json', 'ob-clark-wt-3.json', 'ob-clark-wt-4.json',
    'ob-clark-wt-5.json', 'ob-clark-wt-6.json', 'ob-clark-wt-7.json',
    'ob-clark-wt-8.json', 'ob-clark-wt-9.json', 'ob-clark-wt-10.json',
    'ob-clark-bmi-0.json', 'ob-clark-bmi-1.json',
    'ob-clark-bmi-2.json', 'ob-clark-bmi-3.json', 'ob-clark-bmi-4.json',
    'ob-clark-bmi-5.json', 'ob-clark-bmi-6.json', 'ob-clark-bmi-7.json',
    'ob-clark-bmi-8.json', 'ob-clark-bmi-9.json', 'ob-clark-bmi-10.json',
]
fam_hist_files_clark = ['ob-clark-mth.json', 'ob-clark-fth.json']
rel_person_files_clark = ['rp-clark-mth.json', 'rp-clark-sib.json']

qr_test_dir = 'qr-test'
qr_food_files = ['qresponse-food-insecurity_clark.json', 'qresponse-food-insecurity_kara.json']

tools_dir = 'tools'
this_dir = '.'


def handle(dir_name, files, resource_type):
    client = questionnaire.utils.getFhirClient(questionnaire.utils.MIHIN)
    server = client.server
    for filename in files:
        with open(os.path.join(dir_name, filename), 'r') as h:
            fjson = json.load(h)
            response = server.post_json(resource_type, fjson)
            print response
            # print response.headers


def main():
    # note: comment out what shouldn't be re-uploaded to avoid conflicts
    #       not hardened to detect updates and duplicates!
    handle(obs_dir_kara, obs_files_kara, 'Observation')
    handle(obs_dir_kara, fam_hist_files_kara, 'FamilyMemberHistory')
    handle(obs_dir_kara, rel_person_files_kara, 'RelatedPerson')
    handle(obs_dir_clark, obs_files_clark, 'Observation')
    handle(obs_dir_clark, fam_hist_files_clark, 'FamilyMemberHistory')
    handle(obs_dir_clark, rel_person_files_clark, 'RelatedPerson')
    handle(qr_test_dir, qr_food_files, 'QuestionnaireResponse')

    # one-off load
    # handle(tools_dir, ['questionnaire-wic-child-nutrition.json'],'Questionnaire')


if __name__ == '__main__':
    main()
