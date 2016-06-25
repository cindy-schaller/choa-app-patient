from fhirclient.models import contactpoint, address, humanname
from datetime import datetime

code_root = {"coding": [{
        "system": "http://loinc.org",
        "code": "34565-2",
        "display": "Vital signs, weight and height panel",
}]}

coding_weight = {"coding": [{
            "system": "http://loinc.org",
            "code": "3141-9",
            "display": "Weight"
}]}

coding_height = {"coding": [{
            "system": "http://loinc.org",
            "code": "8302-2",
            "display": "Height"
}]}

coding_bmi = {"coding": [{
            "system": "http://loinc.org",
            "code": "39156-5",
            "display": "BMI"
}]}

kent_telecom = [
        {
            "system":"phone",
            "value":"212.555.1234",
            "use":"home"
        }]

kent_address = [{
    "line":["123 Main Street"],
    "city":"Metropolis",
    "state":"NY",
    "postalCode":"10001" }]
kent_mom_name = [{"family":["Kent"],"given":["Martha"]}]
kent_mom_dob = datetime(1984,2,28)


