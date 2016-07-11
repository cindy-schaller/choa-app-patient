from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import questionnaire, extension
import datetime
from questionnaire_commons import *

def main():
    # set up questionnaire structure from model
    q = questionnaire.Questionnaire()
    root_group = questionnaire.QuestionnaireGroup()
    q.group = root_group
    # root group can be either a group of groups or questions
    questions = []
    root_group.question = questions

    # complete required fields for q level
    q.identifier = [{'value':'questionnaire-healthy-habit-goal-status'}]  # used by response to link to questionnaire
    q.status = 'draft'  #	draft | published | retired

    # complete other fields for q level
    q.publisher = 'GT CS8903 HOC Team'
    q.date = str(datetime.date.today())
    # complete required fields for root group level
    root_group.linkId = 'root'

    # fill in specific data for questions
    # Question 1
    # http://www.hl7.org/fhir/extension-questionnaire-enablewhen.html
    q1 = questionnaire.QuestionnaireGroupQuestion()
    q1.linkId = "1.0"
    q1.text = "What type of progress has been made towards achieving the goal?"
    q1.type = "choice"
    q1.repeats = False
    q1.required = True
    q1.extension = [RADIOBUTTON_EXTENSION, VERTICAL_EXTENSION]
    q1.option = [
        {"code": "a1", "display": "We have already achieved the goal"},
        {"code": "a2", "display": "We are working on the goal"},
        {"code": "a3", "display": "We are not working on the goal"},
    ]
    questions.append(q1)

    # Question 1.1 - followup to achieved goal
    q2 = questionnaire.QuestionnaireGroupQuestion()
    q2.linkId = "1.1"
    q2.text = "If the goal has already achieved the goal is the healthy behavior being maintained?"
    q2.type = "boolean"
    q2.repeats = False
    q2.required = False
    q2.option = YESNO
    # signal that this question should only appear if first question has "a1" as answer
    q2.extension = [{
        "url": QEXT_URL_ENABLEWHEN,
        "extension":[
            {"url": "question","valueString": "1.0"},
            {"url": "answered","valueBoolean": True},
            {"url": "answer","valueCode": "a1"}]
    }]
    questions.append(q2)

    # Question 2
    # TODO make "none" answer c7 non-repeating
    # with current extension coding options, this is complex - not doing it for now
    q3 = questionnaire.QuestionnaireGroupQuestion()
    q3.linkId = "2.0"
    q3.text = "Did any of the following make it difficult to achieve the goal? (Check all that apply)"
    q3.type = "choice"
    q3.repeats = True
    q3.required = True
    q3.extension = [CHECKBOX_EXTENSION]
    q3.option = [
        {"code": "c1", "display": "Lack of time"},
        {"code": "c2", "display": "Lack of resources"},
        {"code": "c3", "display": "Lack of support"},
        {"code": "c4", "display": "Low motivation"},
        {"code": "c5", "display": "Injuries or illness"},
        {"code": "c6", "display": "Other (please specify)"},
        {"code": "c7", "display": "None of the above made it difficult to achieve the goal"},
    ]
    questions.append(q3)

    # Question 2.1 text followup to "other" choice
    q4 = questionnaire.QuestionnaireGroupQuestion()
    q4.linkId = "2.1"
    q4.text = "Please specify Other difficulties"
    q4.type = "text"
    q4.repeats = True
    q4.required = False
    q4.extension = [{
        "url": QEXT_URL_ENABLEWHEN,
        "extension":[
            {"url": "question","valueString": "2.0"},
            {"url": "answered","valueBoolean": True},
            {"url": "answer","valueCode": "c6"}]
    }]
    questions.append(q4)

    with open('questionnaire-healthy-habit-goal-status.json','w') as f:
        print(json.dumps(OrderedDict(q.as_json()), indent=4, separators=(',', ': ')), file=f)


if __name__ == '__main__':
    main()
