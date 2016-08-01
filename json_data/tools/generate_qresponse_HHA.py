from __future__ import print_function
import json
import os
from fhirclient.models import questionnaireresponse, fhirdate
from db_references import *
import datetime
from questionnaire_commons import *

def qr_hha(reference, answers, tag):
    for count,answer_set in enumerate(answers):
        authored_date, int_list = answer_set
        QUESTIONNAIRE_HHA_CHILD_REERENCE = {"reference": "Questionnaire/" + REF_HHA_CHILD}
        # set up questionnaire response structure from model
        qr = questionnaireresponse.QuestionnaireResponse()
        qr.author = reference
        qr.subject = reference
        qr.authored = authored_date
        qr.questionnaire = QUESTIONNAIRE_HHA_CHILD_REERENCE
        qr.status = "completed"
        # build answer group
        qrlist = []
        for i in range(8):
            linkId = 0
            if i <4: linkId = i+1
            elif i >=4: linkId = i+2
            qr_item = {"linkId":str(linkId),"answer":[{"valueInteger":int_list[i]}]}
            qrlist.append(qr_item)
        qr.group = {
            "linkId":"root",
            "question":qrlist
        }
        filename = 'qresponse-hha_' + tag + '_'+str(count)+ '.json'
        #with open(os.path.join('json_data','qr-test', filename),'w') as f:
        # FIXME: for local IDE run
        with open(os.path.join('..','qr-test', filename),'w') as f:
            print(json.dumps(qr.as_json(), indent=4, separators=(',', ': ')), file=f)

def main():
    CLARK_KENT_REFERENCE = {"reference": "Patient/" + REF_CLARK}
    #authored date, answers[1-thru-9]
    clark_md_info = [
        ("2013-03-30T00:00:00",[2,4,3,2,4,4,2,2,]),
        ("2014-06-30T00:00:00",[1,4,3,2,3,1,2,2,]),
        ("2015-06-30T00:00:00",[2,2,3,2,1,3,2,2,]),
    ]
    clark_wic_info = [
        ("2013-03-30T00:00:00",[2,4,3,2,4,4,2,2,]),
        ("2013-09-30T00:00:00",[2,4,3,2,4,4,2,2,]),
        ("2014-03-30T00:00:00",[2,4,3,2,4,4,2,2,]),
        ("2015-07-30T00:00:00",[2,2,3,2,1,3,2,2,]),
        ("2015-09-30T00:00:00", [2,2,3,2,1,3,2,2,]),
        ("2015-12-30T00:00:00", [2,2,3,2,1,3,2,2,]),
        ("2016-03-30T00:00:00", [2,2,3,2,1,3,2,2,]),
    ]
    KARA_KENT_REFERENCE = {"reference": "Patient/" + REF_KARA}
    kara_md_info = [
        ("2014-05-15T00:00:00",[2,2,2,2,2,4,2,2,]),
        ("2015-01-01T00:00:00",[2,2,2,2,2,1,2,2,]),
        ("2015-11-01T00:00:00",[2,3,2,2,2,1,2,2,]),
        ("2016-05-01T00:00:00",[2,4,2,2,2,2,2,2,]),
    ]
    kara_wic_info = [
        ("2014-06-01T00:00:00",[2,2,2,2,2,4,2,2,]),
        ("2014-08-01T00:00:00",[2,2,2,2,2,4,2,2,]),
        ("2014-11-01T00:00:00",[2,2,2,2,2,4,2,2,]),
        ("2015-05-01T00:00:00",[2,2,2,2,2,1,2,2,]),
        ("2015-08-01T00:00:00",[2,2,2,2,2,1,2,2,]),
        ("2016-02-01T00:00:00",[2,4,2,2,2,2,2,2,]),
    ]

    qr_hha(CLARK_KENT_REFERENCE, clark_md_info, "clark")
    qr_hha(KARA_KENT_REFERENCE, kara_md_info, "kara")
    qr_hha(CLARK_KENT_REFERENCE, clark_wic_info, "clark_wic")
    qr_hha(KARA_KENT_REFERENCE, kara_wic_info, "kara_wic")

if __name__ == '__main__':
    main()
