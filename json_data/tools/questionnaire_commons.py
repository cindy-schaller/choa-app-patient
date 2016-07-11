"""
List of common response coding for the questionnaires
"""

YESNO = [
    {'code': True, 'display': 'Yes'},
    {'code': False, 'display': 'No'}
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

CHECKBOX_EXTENSION = [
    {"url": "http://hl7.org/fhir/valueset-questionnaire-question-control.html"},
    {"valueCodeableConcept": {"coding": [{"code": "check-box", "display": "Check-box"}]}},
]

RADIOBUTTON_EXTENSION = [
    {"url": "http://hl7.org/fhir/valueset-questionnaire-question-control.html"},
    {"valueCodeableConcept": {"coding": [{"code": "radio-button", "display": "Radio-button"}]}},
]
