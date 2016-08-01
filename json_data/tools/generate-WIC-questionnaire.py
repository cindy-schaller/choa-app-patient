from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import questionnaire, fhirdate
import datetime
from questionnaire_commons import *

# Q0_FILL = [
#     ("Child's Name:","text",None),
#     ("Date of Birth","text",None),
#     ("Age","text",None),
#     ("Name of Parent/Guardian","text",None),
# ]
# WIC_Q0 = "Child Information", Q0_FILL #nested
#
# text, type, option, linkId, repeats, required, extension
Q1_CHECKBOXES = [
    ("Medicine","boolean", YESNO, "1.0", False, True, None),
    ("If yes, please list:","text", None, "1.1", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"1.0"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("Vitamins/Minerals","boolean", YESNO, "1.2", False, True, None),
    ("If yes, please list:","text", None, "1.3", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"1.2"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("herbal teas/herbal products","boolean", YESNO, "1.4", False, True, None),
    ("If yes, please list:","text", None, "1.5", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"1.4"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("Home remedies","boolean", YESNO, "1.6", False, True, None),
    ("If yes, please list:","text", None, "1.7", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"1.6"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    # TODO "none" should not be offered if anything else checked
    ("none","boolean", YESNO, "1.8", False, False, None),
]
WIC_Q1 = "1. Check all that your child takes: ", Q1_CHECKBOXES
Q2_CHECKBOXES = [
    ("breast","boolean", YESNO, "2.0", False, True, None),
    ("baby bottle","boolean", YESNO, "2.1", False, True, None),
    ("sippy cup","boolean", YESNO, "2.2", False, True, None),
    ("his/her fingers","boolean", YESNO, "2.3", False, True, None),
    ("regular cup","boolean", YESNO, "2.4", False, True, None),
    ("spoon or fork","boolean", YESNO, "2.5", False, True, None),
    ("other","boolean", YESNO, "2.6", False, True, None),
    ("If other, please list:", "text", None, "2.7", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"2.6"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
]
WIC_Q2 = "2. Check all that your child uses to eat or drink:",Q2_CHECKBOXES
Q3_CHECKBOXES = [
    ("Does your child skip meals or have a limited amount of food at meals because there is not enough money to buy food?","boolean", YESNO, "3.0", False, True, None),
]
WIC_Q3 = "3. ", Q3_CHECKBOXES
Q4_CHECKBOXES = [
    ("Do you have a working stove, refrigerator, and sink?","boolean", YESNO, "4.0", False, True, None),
]
WIC_Q4 = "4. ", Q4_CHECKBOXES
Q5_CHECKBOXES = [
    ("Meat, poultry, fish, beans, or eggs", "integer", HOW_OFTEN_DAILY_3WAY, "5.0", False, True, None),
    ("Milk, yogurt, or cheese", "integer", HOW_OFTEN_DAILY_3WAY, "5.1", False, True, None),
    ("Fruits", "integer", HOW_OFTEN_DAILY_3WAY, "5.2", False, True, None),
    ("Vegetables", "integer", HOW_OFTEN_DAILY_3WAY, "5.3", False, True, None),
    ("Grains- cereal, bread, rice, pasta, tortillas", "integer", HOW_OFTEN_DAILY_3WAY, "5.4", False, True, None),
    ("Cookies, cakees, pies, candy", "integer", HOW_OFTEN_DAILY_3WAY, "5.5", False, True, None),
    ("Fried foods, french fries, sausage, hot dogs, bacon", "integer", HOW_OFTEN_DAILY_3WAY, "5.6", False, True, None),
]
WIC_Q5 = "5. Check how often your child eats these foods", Q5_CHECKBOXES
Q6_CHECKBOXES = [
    ("breast milk", "boolean", YESNO, "6.0", False, True, None),
    ("whole milk", "boolean", YESNO, "6.1", False, True, None),
    ("2% reduced fat milk", "boolean", YESNO, "6.2", False, True, None),
    ("1% reduced fat milk", "boolean", YESNO, "6.3", False, True, None),
    ("fat free milk", "boolean", YESNO, "6.4", False, True, None),
    ("soy milk", "boolean", YESNO, "6.5", False, True, None),
    ("water", "boolean", YESNO, "6.6", False, True, None),
    ("fruit drink", "boolean", YESNO, "6.7", False, True, None),
    ("100% fruit juice", "boolean", YESNO, "6.8", False, True, None),
    ("soda", "boolean", YESNO, "6.9", False, True, None),
    ("Gatorade", "boolean", YESNO, "6.10", False, True, None),
    ("tea", "boolean", YESNO, "6.11", False, True, None),
    ("other", "boolean", YESNO, "6.12", False, True, None),
    ("If other, please list:", "text", None, "6.13", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"6.12"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
]
WIC_Q6 = "6. Check all that your child drinks:",Q6_CHECKBOXES
Q7_CHECKBOXES = [
    ("hard candies", "boolean", YESNO, "7.0", False, True, None),
    ("Gum drops", "boolean", YESNO, "7.1", False, True, None),
    ("chewing gum", "boolean", YESNO, "7.2", False, True, None),
    ("chips", "boolean", YESNO, "7.3", False, True, None),
    ("popcorn", "boolean", YESNO, "7.4", False, True, None),
    ("pretzels", "boolean", YESNO, "7.5", False, True, None),
    ("nuts", "boolean", YESNO, "7.6", False, True, None),
    ("spoonfuls of peanut butter", "boolean", YESNO, "7.7", False, True, None),
    ("seeds", "boolean", YESNO, "7.8", False, True, None),
    ("raisins", "boolean", YESNO, "7.9", False, True, None),
    ("dried fruit", "boolean", YESNO, "7.10", False, True, None),
    ("whole grapes", "boolean", YESNO, "7.11", False, True, None),
    ("hot dogs", "boolean", YESNO, "7.12", False, True, None),
    ("uncooked meat", "boolean", YESNO, "7.13", False, True, None),
    ("uncooked fish", "boolean", YESNO, "7.14", False, True, None),
    ("uncooked eggs", "boolean", YESNO, "7.15", False, True, None),
    ("dirt", "boolean", YESNO, "7.16", False, True, None),
    ("clay", "boolean", YESNO, "7.17", False, True, None),
    ("chalk", "boolean", YESNO, "7.18", False, True, None),
    ("ashes", "boolean", YESNO, "7.19", False, True, None),
    ("laundry starch", "boolean", YESNO, "7.20", False, True, None),
    ("Cornstarch", "boolean", YESNO, "7.21", False, True, None),
    ("baking soda", "boolean", YESNO, "7.22", False, True, None),
    ("crayons", "boolean", YESNO, "7.23", False, True, None),
    ("large amounts of ice", "boolean", YESNO, "7.24", False, True, None),
]
WIC_Q7 = "7. Check all that your child eats:", Q7_CHECKBOXES
Q8_CHECKBOXES = [
    ("Does your child eat fast food meals more than 2 times a week?", "boolean", YESNO, "8.0", False, True, None),
]
WIC_Q8 = "8. ", Q8_CHECKBOXES
Q9_SUBQUESTIONS = [
    ("How do you know when your child is hungry?","text",None, "9.0", False, False, None),
    ("How do you know when your child is full?","text",None, "9.1", False, False, None),
]
WIC_Q9 = "9. ",Q9_SUBQUESTIONS
Q10_CHECKBOXES = [
    ("regular health check-ups?","boolean", YESNO, "10.0", False, True, None),
    ("regular dental check-ups?", "boolean", YESNO, "10.1", False, True, None),
]
WIC_Q10 = "10. Does your child go for:",Q10_CHECKBOXES
Q11_CHECKBOXES = [
    ("diarrhea", "boolean", YESNO, "11.0", False, True, None),
    ("constipation", "boolean", YESNO, "11.1", False, True, None),
    ("vomiting", "boolean", YESNO, "11.2", False, True, None),
    ("nausea", "boolean", YESNO, "11.3", False, True, None),
    ("difficulty chewing or swallowing", "boolean", YESNO, "11.4", False, True, None),
    ("unable to feed self", "boolean", YESNO, "11.5", False, True, None),
    ("dental problems", "boolean", YESNO, "11.6", False, True, None),
    ("special diet", "boolean", YESNO, "11.7", False, True, None),
    ("if yes, enter special diet:", "text", None, "11.8", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"11.7"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("health or medical problem", "boolean", YESNO, "11.9", False, True, None),
    ("if yes, enter or medical problem:", "text", None, "11.10", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"11.9"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("food allergy or problem", "boolean", YESNO, "11.11", False, True, None),
    ("if yes, enter allergy or problem:", "text", None, "11.12", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"11.11"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
    ("none", "boolean", YESNO, "11.13", False, True, None),
]
WIC_Q11 = "11. Check all your child has had in the last month:",Q11_CHECKBOXES
Q12_CHECKBOXES = [
    ("What is your child's usual daily activity?","integer", HOW_ACTIVE_DAILY_3WAY, "12.0", False, True, None),
]
WIC_Q12 = "12. ",Q12_CHECKBOXES
Q13_CHECKBOXES = [
    ("How many hours a day does your child watch TV, play at the computer, or play video games?","text", None, "13.0", False, False, None),
]
WIC_Q13 = "13. ",Q13_CHECKBOXES
Q14_CHECKBOXES = [
    ("Does your child eat meals provided by a child care center or at school?","boolean", YESNO, "14.0", False, True, None),
]
WIC_Q14 = "14. ",Q14_CHECKBOXES
Q15_SUBQUESTIONS = [
    ("Do you have any questions or concerns about your child's health, diet, feeding, or growth?","boolean",YESNO, "15.0", False, True, None),
    ("If yes, please describe","text",None, "15.1", False, False, [{
        "url":QEXT_URL_ENABLEWHEN,
        "extension":[{"url":"question","valueString":"15.0"},
                     {"url":"answered","valueBoolean":True},
                     {"url":"answer","valueBoolean":True}]}]),
]
WIC_Q15 = "15. ", Q15_SUBQUESTIONS
Q16_SUBQUESTIONS = [
    ("Please offer any suggestions on what WIC can do to better serve you and your family.","text",None, "16.0", False, False, None),
]
WIC_Q16 = "16. ", Q16_SUBQUESTIONS

WIC_QUESTIONS = [
    # WIC_Q0,
    WIC_Q1,
    WIC_Q2, WIC_Q3, WIC_Q4, WIC_Q5, WIC_Q6, WIC_Q7, WIC_Q8,
    WIC_Q9, WIC_Q10, WIC_Q11, WIC_Q12, WIC_Q13, WIC_Q14, WIC_Q15, WIC_Q16,
]


def isNested(param):
    if param is None: return True
    else: return False

if __name__ == '__main__':
    # set up questionnaire structure from model
    q = questionnaire.Questionnaire()
    root_group = questionnaire.QuestionnaireGroup()
    q.group = root_group

    # complete required fields for q level
    q.identifier = [{'value': 'questionnaire-wic-child-nutrition'}]  # used by response to link to questionnaire
    q.status = 'draft'  # draft | published | retired

    # complete other fields for q level
    q.publisher = 'GT CS8903 HOC Team'
    q.date = str(datetime.date.today())

    # complete fields for root group level
    root_group.linkId = 'root'
    root_group.title = 'WIC Child Nutrition Questionnaire'

    # root group can be either a group of groups or questions
    questions_group = []
    root_group.group = questions_group

    # for each wic question, create a QuestionnaireGroup obj to add to the list
    # then for each QuestionnaireGroup obj, assign the question to a list of QuestionnaireGroupQuestion objects
    for i, wic_question_tuple in enumerate(WIC_QUESTIONS):
        q_group = questionnaire.QuestionnaireGroup()
        grp_text, question_details = wic_question_tuple
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




    with open('questionnaire-wic-child-nutrition.json', 'w') as f:
        print(json.dumps(q.as_json(), indent=4, separators=(',', ': ')), file=f)
