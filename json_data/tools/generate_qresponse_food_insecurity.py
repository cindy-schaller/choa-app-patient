from __future__ import print_function
import json
from fhirclient.models import questionnaireresponse, fhirdate
import datetime
from questionnaire_commons import *
CDC_QUESTIONS = [
    "In the last year, did you worry that your food would run out before you got money or Food Stamps to buy more?",
    "In the last year, did the food you bought just not last and you didn't have money to get more?",
]
CLARK_KENT_REFERENCE = {"reference":"Patient/11034584"}
KARA_KENT_REFERENCE = {"reference":"Patient/11037781"}
QUESTIONNAIRE_FOOD_INSECURITY_REERENCE = {"reference":"Questionnaire/11036849"}

def qr_food(reference, is_insecure, tag):
    # set up questionnaire response structure from model
    qr = questionnaireresponse.QuestionnaireResponse()
    qr.author = reference
    qr.subject = reference
    qr.authored = "2016-06-30T19:05:47.356000"
    qr.questionnaire = QUESTIONNAIRE_FOOD_INSECURITY_REERENCE
    qr.status = "completed"
    qr.group = {
        "linkId":"root",
        "question":[
            {"linkId":"1","answer":[{"valueBoolean":is_insecure}]},
            {"linkId":"2","answer":[{"valueBoolean":is_insecure}]},
        ]
    }

    with open('qresponse-food-insecurity_' + tag + '.json','w') as f:
        print(json.dumps(qr.as_json(), indent=4, separators=(',', ': ')), file=f)

def main():
    qr_food(CLARK_KENT_REFERENCE, True, "clark")
    qr_food(KARA_KENT_REFERENCE, True, "kara")

if __name__ == '__main__':
    main()
