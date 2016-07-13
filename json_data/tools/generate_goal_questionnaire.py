from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import questionnaire, fhirdate
import datetime
from questionnaire_commons import *
GOAL_QUESTIONS = [
    "How will you work with your child on this goal?",
    "When will you work with your child on this goal?",
    "How often will you work with your child on this goal?",
    "Who can support you?",
    "When will you start working on your child's goal?)",
    "What barriers may stop you from supporting your child's goal?",
    "Other Notes:",
    ]
def main():
    # set up questionnaire structure from model
    q = questionnaire.Questionnaire()
    root_group = questionnaire.QuestionnaireGroup()
    q.group = root_group
    # root group can be either a group of groups or questions
    questions = []
    root_group.question = questions

    # complete required fields for q level
    q.identifier = [{'value':'questionnaire-healthy-habit-goals'}]  # used by response to link to questionnaire
    q.status = 'draft'  #	draft | published | retired

    # complete other fields for q level
    q.publisher = 'GT CS8903 HOC Team'
    q.date = str(datetime.date.today())
    # complete required fields for root group level
    root_group.linkId = 'root'

    # fill in specific data for questions
    for i in range(len(GOAL_QUESTIONS)):
        item = questionnaire.QuestionnaireGroupQuestion()
        item.linkId = str(i+1)
        item.text = GOAL_QUESTIONS[i]
        item.type = 'string'
        item.required = True
        item.repeats = False
        questions.append(item)

    with open('questionnaire-healthy-habit-goals.json','w') as f:
        print(json.dumps(OrderedDict(q.as_json()), indent=4, separators=(',', ': ')), file=f)


if __name__ == '__main__':
    main()
