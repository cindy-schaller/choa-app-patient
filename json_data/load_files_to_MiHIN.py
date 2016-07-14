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
rel_person_files_clark = ['rp-clark-mth.json','rp-clark-sib.json']
this_dir = '.'


def handle(dir_name, files, resource_type):
    client = questionnaire.utils.getFhirClient(questionnaire.utils.MIHIN)
    server = client.server
    for filename in files:
        with open(os.path.join(dir_name, filename), 'r') as h:
            fjson = json.load(h)
            response = server.post_json(resource_type, fjson)
            print response
            print response.headers


def main():
    # note: comment out what shouldn't be re-uploaded to avoid conflicts
    #       not hardened to detect updates and duplicates!
    # handle(obs_dir_kara, obs_files_kara, 'Observation')
    # handle(obs_dir_kara, fam_hist_files_kara, 'FamilyMemberHistory')
    # handle(obs_dir_kara, rel_person_files_kara, 'RelatedPerson')
    # handle(obs_dir_clark, rel_person_files_clark, 'RelatedPerson')

    # one-off load
    handle(this_dir, ['qresponse-food-insecurity.json'],'QuestionnaireResponse')
    # handle(obs_dir_clark, ['rp-clark-sib.json'] , 'RelatedPerson')
    # handle(obs_dir_kara, ['rp-kara-sib.json'] , 'RelatedPerson')



if __name__ == '__main__':
    main()
