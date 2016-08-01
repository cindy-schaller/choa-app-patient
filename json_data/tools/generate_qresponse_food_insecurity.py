from __future__ import print_function
import json
import os
from fhirclient.models import questionnaireresponse, fhirdate
from db_references import *
import datetime
from questionnaire_commons import *

def qr_food(date_authored, patient_reference, might_run_out, did_run_out, tag):
    CDC_QUESTIONS = [
        "In the last year, did you worry that your food would run out before you got money or Food Stamps to buy more?",
        "In the last year, did the food you bought just not last and you didn't have money to get more?",
    ]
    QUESTIONNAIRE_FOOD_INSECURITY_REERENCE = {"reference": "Questionnaire/" + REF_INSECURITY}
    # set up questionnaire response structure from model
    qr = questionnaireresponse.QuestionnaireResponse()
    qr.source = patient_reference
    qr.subject = patient_reference
    qr.authored = date_authored
    qr.questionnaire = QUESTIONNAIRE_FOOD_INSECURITY_REERENCE
    qr.status = "completed"
    qr.group = {
        "linkId":"root",
        "question":[
            {"linkId":"1","answer":[{"valueBoolean":might_run_out}]},
            {"linkId":"2","answer":[{"valueBoolean":did_run_out}]},
        ]
    }
    filename = 'qresponse-food-insecurity_' + tag + '.json'
    #FIXME local requires different join than call from django command
    #with open(os.path.join('..','qr-test', filename),'w') as f:
    with open(os.path.join('json_data','qr-test', filename),'w') as f:
        print(json.dumps(qr.as_json(), indent=4, separators=(',', ': ')), file=f)

def main():
    CLARK_KENT_REFERENCE = {"reference": "Patient/" + REF_CLARK}
    KARA_KENT_REFERENCE = {"reference": "Patient/" + REF_KARA}
    qr_food("2013-03-30T13:00:00",CLARK_KENT_REFERENCE, True, False, "clark_tf")
    qr_food("2014-06-30T13:00:00",CLARK_KENT_REFERENCE, False, True, "clark_ft")
    qr_food("2015-06-30T13:00:00",CLARK_KENT_REFERENCE, False, False, "clark_ff")
    qr_food("2016-06-30T13:00:00",CLARK_KENT_REFERENCE, True, True, "clark_tt")
    qr_food("2014-05-15T13:00:00",KARA_KENT_REFERENCE, True, False, "kara_tf")
    qr_food("2015-01-01T13:00:00",KARA_KENT_REFERENCE, False, True, "kara_ft")
    qr_food("2015-11-01T13:00:00",KARA_KENT_REFERENCE, False, False, "kara_ff")
    qr_food("2016-06-30T13:00:00",KARA_KENT_REFERENCE, True, True, "kara_tt")

if __name__ == '__main__':
    main()
