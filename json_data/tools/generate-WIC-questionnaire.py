from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import questionnaire, fhirdate
import datetime
from questionnaire_commons import *

Q0_FILL = [
    ("Child's Name:","text",None),
    ("Date of Birth","text",None),
    ("Age","text",None),
    ("Name of Parent/Guardian","text",None),
]
WIC_Q0 = "Child Information", Q0_FILL #nested
Q1_CHECKBOXES = [
    ("Medicine","boolean", YESNO),
    ("If yes, please list:","text", None),
    ("Vitamins/Minerals","boolean", YESNO),
    ("If yes, please list:","text", None),
    ("herbal teas/herbal products","boolean", YESNO),
    ("If yes, please list:","text", None),
    ("Home remedies","boolean", YESNO),
    ("If yes, please list:","text", None),
    ("none","boolean", YESNO),  # TODO should not be offered if anything else checked
]
WIC_Q1 = "1. Check all that your child takes: ", Q1_CHECKBOXES
Q2_CHECKBOXES = [
    ("breast","boolean", YESNO),
    ("baby bottle","boolean", YESNO),
    ("sippy cup","boolean", YESNO),
    ("his/her fingers","boolean", YESNO),
    ("regular cup","boolean", YESNO),
    ("spoon or fork","boolean", YESNO),
    ("other","boolean", YESNO),
    ("If other, please list:", "text", None),
]
WIC_Q2 = "2. Check all that your child uses to eat or drink:",Q2_CHECKBOXES
Q3_CHECKBOXES = [
    ("Does your child skip meals or have a limited amount of food at meals because there is not enough money to buy food?","boolean", YESNO)
]
WIC_Q3 = "3. ", Q3_CHECKBOXES
Q4_CHECKBOXES = [
    ("Do you have a working stove, refrigerator, and sink?","boolean", YESNO)
]
WIC_Q4 = "4. ", Q4_CHECKBOXES
Q5_CHECKBOXES = [
    ("Meat, poultry, fish, beans, or eggs", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Milk, yogurt, or cheese", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Fruits", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Vegetables", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Grains- cereal, bread, rice, pasta, tortillas", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Cookies, cakees, pies, candy", "integer", HOW_OFTEN_DAILY_3WAY),
    ("Fried foods, french fries, sausage, hot dogs, bacon", "integer", HOW_OFTEN_DAILY_3WAY),
]
WIC_Q5 = "5. Check how often your child eats these foods", Q5_CHECKBOXES
Q6_CHECKBOXES = [
    ("breast milk", "boolean", YESNO),
    ("whole milk", "boolean", YESNO),
    ("2% reduced fat milk", "boolean", YESNO),
    ("1% reduced fat milk", "boolean", YESNO),
    ("fat free milk", "boolean", YESNO),
    ("soy milk", "boolean", YESNO),
    ("water", "boolean", YESNO),
    ("fruit drink", "boolean", YESNO),
    ("100% fruit juice", "boolean", YESNO),
    ("soda", "boolean", YESNO),
    ("Gatorade", "boolean", YESNO),
    ("tea", "boolean", YESNO),
    ("other", "boolean", YESNO),
    ("If other, please list:", "text", None),
]
WIC_Q6 = "6. Check all that your child drinks:",Q6_CHECKBOXES
Q7_CHECKBOXES = [
    ("hard candies", "boolean", YESNO),
    ("Gum drops", "boolean", YESNO),
    ("chewing gum", "boolean", YESNO),
    ("chips", "boolean", YESNO),
    ("popcorn", "boolean", YESNO),
    ("pretzels", "boolean", YESNO),
    ("nuts", "boolean", YESNO),
    ("spoonfuls of peanut butter", "boolean", YESNO),
    ("seeds", "boolean", YESNO),
    ("raisins", "boolean", YESNO),
    ("dried fruit", "boolean", YESNO),
    ("whole grapes", "boolean", YESNO),
    ("hot dogs", "boolean", YESNO),
    ("uncooked meat", "boolean", YESNO),
    ("uncooked fish", "boolean", YESNO),
    ("uncooked eggs", "boolean", YESNO),
    ("dirt", "boolean", YESNO),
    ("clay", "boolean", YESNO),
    ("chalk", "boolean", YESNO),
    ("ashes", "boolean", YESNO),
    ("laundry starch", "boolean", YESNO),
    ("Cornstarch", "boolean", YESNO),
    ("baking soda", "boolean", YESNO),
    ("crayons", "boolean", YESNO),
    ("large amounts of ice", "boolean", YESNO),
]
WIC_Q7 = "7. Check all that your child eats:", Q7_CHECKBOXES
Q8_CHECKBOXES = [
    ("Does your child eat fast food meals more than 2 times a week?", "boolean", YESNO)
]
WIC_Q8 = "8. ", Q8_CHECKBOXES
Q9_SUBQUESTIONS = [
    ("How do you know when your child is hungry?","text",None),
    ("How do you know when your child is full?","text",None),
]
WIC_Q9 = "9. ",Q9_SUBQUESTIONS
Q10_CHECKBOXES = [
    ("regular health check-ups?","boolean", YESNO),
    ("regular dental check-ups?", "boolean", YESNO),
]
WIC_Q10 = "10. Does your child go for:",Q10_CHECKBOXES
Q11_CHECKBOXES = [
    ("diarrhea", "boolean", YESNO),
    ("constipation", "boolean", YESNO),
    ("vomiting", "boolean", YESNO),
    ("nausea", "boolean", YESNO),
    ("difficulty chewing or swallowing", "boolean", YESNO),
    ("unable to feed self", "boolean", YESNO),
    ("dental problems", "boolean", YESNO),
    ("special diet", "boolean", YESNO),
    ("if yes, enter special diet:", "text", None),
    ("health or medical problem", "boolean", YESNO),
    ("if yes, enter or medical problem:", "text", None),
    ("food allergy or problem", "boolean", YESNO),
    ("if yes, enter allergy or problem:", "text", None),
    ("none", "boolean", YESNO),
]
WIC_Q11 = "11. Check all your child has had in the last month:",Q11_CHECKBOXES
Q12_CHECKBOXES = [
    ("What is your child's usual daily activity?","integer", HOW_ACTIVE_DAILY_3WAY)
]
WIC_Q12 = "12. ",Q12_CHECKBOXES
Q13_CHECKBOXES = [
    ("How many hours a day does your child watch TV, play at the computer, or play video games?","text", None)
]
WIC_Q13 = "13. ",Q13_CHECKBOXES
Q14_CHECKBOXES = [
    ("Does your child eat meals provided by a child care center or at school?","boolean", YESNO)
]
WIC_Q14 = "14. ",Q14_CHECKBOXES
Q15_SUBQUESTIONS = [
    ("Do you have any questions or concerns about your child's health, diet, feeding, or growth?","boolean",YESNO),
    ("If yes, please describe","text",None),
]
WIC_Q15 = "15. Check all your child has had in the last month:", Q15_SUBQUESTIONS
Q16_SUBQUESTIONS = [
    ("Please offer any suggestions on what WIC can do to better serve you and your family.","text",None)
]
WIC_Q16 = "16. ", Q16_SUBQUESTIONS

WIC_QUESTIONS = [
    WIC_Q0,
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

    # root group can be either a group of groups or questions
    questions_group = []
    root_group.group = questions_group

    # for each wic question, create a QuestionnaireGroup obj to add to the list
    # then for each QuestionnaireGroup obj, assign the question to a list of QuestionnaireGroupQuestion objects
    for i, wic_question_tuple in enumerate(WIC_QUESTIONS):
        q_group = questionnaire.QuestionnaireGroup()
        grp_text, question_details = wic_question_tuple
        q_group.text = grp_text
        q_group.linkId = str(i)
        questions_group.append(q_group)

        questions = []
        q_group.question = questions
        for j, sub_q_truple in enumerate(question_details):
            q_question = questionnaire.QuestionnaireGroupQuestion()
            q_question.linkId = str(i) + "." + str(j)
            q_question.text, q_question.type, option = sub_q_truple
            if option is not None: q_question.option = option
            q_question.repeats = False
            q_question.required = True
            questions.append(q_question)




    with open('questionnaire-wic-child-nutrition.json', 'w') as f:
        print(json.dumps(q.as_json(), indent=4, separators=(',', ': ')), file=f)
