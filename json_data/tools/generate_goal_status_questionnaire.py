from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import questionnaire, extension
import datetime
from questionnaire_commons import *

STATUS_3WAY = [
    {'code': '1', 'display': 'We have already achieved the goal'},
    {'code': '2', 'display': 'We are working on the goal'},
    {'code': '3', 'display': 'We are not working on the goal'},
]
Q1_CHECKBOXES = [
    ("What type of progress has been made towards achieving the goal?",
     "integer", STATUS_3WAY, "1.1", False, True, None),
]
ST_Q1 = "1. ",Q1_CHECKBOXES
Q2_CHECKBOXES = [
    ("If the goal has already been achieved, is the healthy behavior being maintained?",
     "integer",YESNONA, "2.1", False, False, None),
]
ST_Q2 = "2. ",Q2_CHECKBOXES

# represent checkbox choices as nested yes/no in group
Q3_CHECKBOXES = [
    ("Lack of time", "boolean", YESNO, "3.1", False, True, None),
    ("Lack of resources", "boolean", YESNO, "3.2", False, True, None),
    ("Lack of support", "boolean", YESNO, "3.3", False, True, None),
    ("Low motivation", "boolean", YESNO, "3.4", False, True, None),
    ("Injuries or illness", "boolean", YESNO, "3.5", False, True, None),
    ("Other", "boolean", YESNO, "3.6", False, True, None),
    ("If Other, please specify:", "text", None, "3.7", False, False, [{
        "url": QEXT_URL_ENABLEWHEN,
        "extension": [{"url": "question", "valueString": "3.6"},
                      {"url": "answered", "valueBoolean": True},
                      {"url": "answer", "valueBoolean": True}]}]),
    ("None of the above made it difficult to achieve the goal", "integer", YESNONA, "3.8", False, False, None),
]
ST_Q3 = "3. Did any of the following make it difficult to achieve the goal?",Q3_CHECKBOXES
ST_QUESTIONS = [
    ST_Q1, ST_Q2, ST_Q3
]

def main():
    # set up questionnaire structure from model
    q = questionnaire.Questionnaire()
    root_group = questionnaire.QuestionnaireGroup()
    q.group = root_group
    # root group can be either a group of groups or questions

    # complete required fields for q level
    q.identifier = [{'value':'questionnaire-healthy-habit-goal-status'}]  # used by response to link to questionnaire
    q.status = 'draft'  #	draft | published | retired

    # complete other fields for q level
    q.publisher = 'GT CS8903 HOC Team'
    q.date = str(datetime.date.today())

    # complete required fields for root group level
    root_group.linkId = 'root'
    root_group.title = 'Healthy Habits Goal Status'

    # root group can be either a group of groups or questions
    questions_group = []
    root_group.group = questions_group

    # for each status question, create a QuestionnaireGroup obj to add to the list
    # then for each QuestionnaireGroup obj, assign the question to a list of QuestionnaireGroupQuestion objects
    for i, st_question_tuple in enumerate(ST_QUESTIONS):
        q_group = questionnaire.QuestionnaireGroup()
        grp_text, question_details = st_question_tuple
        q_group.text = grp_text
        q_group.linkId = str(i+1)
        questions_group.append(q_group)

        questions = []
        q_group.question = questions
        for j, sub_q_truple in enumerate(question_details):
            q_question = questionnaire.QuestionnaireGroupQuestion()
            q_question.linkId = str(i) + "." + str(j)
            q_question.text, q_question.type, option, q_question.linkId, q_question.repeats,\
            q_question.required, extension = sub_q_truple
            if option is not None: q_question.option = option
            if extension is not None: q_question.extension = extension
            questions.append(q_question)

    with open('questionnaire-healthy-habit-goal-status.json','w') as f:
        print(json.dumps(OrderedDict(q.as_json()), indent=4, separators=(',', ': ')), file=f)


if __name__ == '__main__':
    main()
