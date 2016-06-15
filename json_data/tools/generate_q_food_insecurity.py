import json
from collections import OrderedDict
from fhirclient.models import questionnaire, fhirdate
import datetime

CDC_QUESTIONS = [
    "In the last year, did you worry that your food would run out before you got money or Food Stamps to buy more?",
    "In the last year, did the food you bought just not last and you didn't have money to get more?",
]

if __name__ == '__main__':
    # set up questionnaire structure from model
    q = questionnaire.Questionnaire()
    root_group = questionnaire.QuestionnaireGroup()
    q.group = root_group
    # root group can be either a group of groups or questions
    questions = []
    root_group.question = questions

    # complete required fields for q level
    q.identifier = [{'value':'questionnaire-food-insecurity'}]  # used by response to link to questionnaire
    q.status = 'draft'  #	draft | published | retired

    # complete other fields for q level
    q.publisher = 'GT CS8903 HOC Team'
    q.date = str(datetime.date.today())
    # complete required fields for root group level
    root_group.linkId = 'root'

    # fill in specific data for questions
    for i in range(1,3):
        item = questionnaire.QuestionnaireGroupQuestion()
        item.linkId = str(i)
        item.text = CDC_QUESTIONS[i-1]
        item.type = 'integer'
        item.required = True
        item.repeats = False
        item.option = [{'code':'1', 'display':'Yes'},
                       {'code':'2', 'display':'No'}]
        questions.append(item)

    with open('questionnaire-food-insecurity.json','w') as f:
        print(json.dumps(OrderedDict(q.as_json()), indent=4, separators=(',', ': ')), file=f)
