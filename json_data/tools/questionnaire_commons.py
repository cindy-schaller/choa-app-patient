"""
List of common response coding for the questionnaires
"""

YESNO = [
    {'code': True, 'display': 'Yes'},
    {'code': False, 'display': 'No'}
]

YESNONA = [
    {'code': '1', 'display': 'Yes'},
    {'code': '2', 'display': 'No'},
    {'code': '0', 'display': 'Not applicable'},
]

HOW_OFTEN_DAILY_3WAY = [
    {'code': '1', 'display': 'Daily'},
    {'code': '2', 'display': 'Some days'},
    {'code': '3', 'display': 'Never'},
]

HOW_ACTIVE_DAILY_3WAY = [
    {'code': '1', 'display': 'Very active (plays actively 2 or more hours per day)'},
    {'code': '2', 'display': 'Active some of the time (plays actively about 1 to 2 hours per day)'},
    {'code': '3', 'display': 'not active'},
]

# Questionnaire Core Extensions
# https://www.hl7.org/fhir/questionnaire-extensions.html
QEXT_URL_QUESTION_CONTROL = "http://hl7.org/fhir/valueset-questionnaire-question-control.html"
QEXT_URL_ENABLEWHEN = "http://hl7.org/fhir/StructureDefinition/questionnaire-enableWhen"
QEXT_URL_CHOICEORIENTATION = "http://www.hl7.org/fhir/extension-questionnaire-choiceorientation.html"

CHECKBOX_EXTENSION = {
    "url": QEXT_URL_QUESTION_CONTROL,
    "valueCodeableConcept": {"coding": [{"code": "check-box", "display": "Check-box"}]}
}

RADIOBUTTON_EXTENSION = {
    "url": QEXT_URL_QUESTION_CONTROL,
    "valueCodeableConcept": {"coding": [{"code": "radio-button", "display": "Radio-button"}]}
}

HORIZONTAL_EXTENSION = {
    "url": QEXT_URL_CHOICEORIENTATION,
    "valueCode": "horizontal"
}

VERTICAL_EXTENSION = {
    "url": QEXT_URL_CHOICEORIENTATION,
    "valueCode": "vertical"
}

