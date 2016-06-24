# basic method to load to MiHIN
# should make nicer and add to loaders in django management
import os
import json
import utils

obs_dir = 'ob-kara'
obs_files = ['ob-kara-ht-0.json', 'ob-kara-ht-1.json', 'ob-kara-ht-2.json',
             'ob-kara-ht-3.json', 'ob-kara-ht-4.json', 'ob-kara-ht-5.json',
             'ob-kara-ht-6.json', 'ob-kara-ht-7.json', 'ob-kara-ht-8.json',
             'ob-kara-ht-9.json', 'ob-kara-wt-0.json', 'ob-kara-wt-1.json',
             'ob-kara-wt-2.json', 'ob-kara-wt-3.json', 'ob-kara-wt-4.json',
             'ob-kara-wt-5.json', 'ob-kara-wt-6.json', 'ob-kara-wt-7.json',
             'ob-kara-wt-8.json', 'ob-kara-wt-9.json']
fam_hist_files = ['ob-kara-mth.json', 'ob-kara-fth.json']

def handle(dir_name,files,resource_type):
    client = utils.getFhirClient(utils.MIHIN)
    server = client.server
    for filename in files:
        with open(os.path.join(dir_name,filename), 'r') as h:
            fjson = json.load(h)
            response = server.post_json(resource_type,fjson)
            print response

def main():
    handle(obs_dir,obs_files,'Observation')
    handle(obs_dir,fam_hist_files,'FamilyMemberHistory')

if __name__ == '__main__':
    main()
