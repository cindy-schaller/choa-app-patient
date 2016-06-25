from __future__ import print_function
import json
import os
from collections import OrderedDict
from fhirclient.models import fhirdate, observation, patient, familymemberhistory, quantity, relatedperson
from observation_commons import *
from datetime import datetime
from dateutil.relativedelta import relativedelta

patient_id = "11034584"
patient_id_ref = "Patient/"+patient_id
patient_name = "Clark Kent"
patient_dob = kent_clark_dob

# Observation/11037412/_history/1
# data for generation (provided by Aly)
# Boy Smith 2-5 yr
# Visit    Age(mos)   Wt(lbs)  Ht(in)  BMI(kg/m2)
observation_list = [
    ["MD",  24, 30., 34.5, 17.7],
    ["WIC", 24, 30., 34.5, 17.7],
    ["WIC", 30, 34., 36.25, 18],
    ["WIC", 36, 36., 38., 17.5],
    ["MD",  39, 38., 38.25, 18],
    ["WIC", 48, 44., 40., 19],
    ["MD",  51, 44., 40., 19],
    ["WIC", 52, 44., 40., 19],
    ["WIC", 54, 46., 40.25, 19.9],
    ["WIC", 57, 46.5, 40.5, 19.9],
    ["WIC", 60, 48., 42., 19.1],
]

def lbs_to_kg(lbs):
    return round(lbs*0.453592,1)
def in_to_cm(ins):
    return round(ins*2.54,1)
def gen_obs():
    # set up observation structure from model
    for i in range(len(observation_list)):
        performer, age_mos, wt_lbs, ht_in, bmi = observation_list[i]
        o = observation.Observation()
        o.status = 'final'
        o.subject = {"reference": patient_id_ref, "display": patient_name}
        o.encounter = [{"display": performer}]
        o.performer = [{"display": performer}]
        date_seen = patient_dob + relativedelta(months=age_mos)
        o.effectiveDateTime = date_seen.isoformat()

        o.code = coding_weight
        o.valueQuantity = {"value": lbs_to_kg(wt_lbs), "unit": "kg"}
        with open(os.path.join('../ob-clark', 'ob-clark-wt-' + str(i) + '.json'), 'w') as f:
            print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)

        o.code = coding_height
        o.valueQuantity = {"value": in_to_cm(ht_in), "unit": "cm"}
        with open(os.path.join('../ob-clark', 'ob-clark-ht-' + str(i) + '.json'), 'w') as f:
            print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)

        o.code = coding_bmi
        o.valueQuantity = {"value": bmi, "unit": "kg/m2"}
        with open(os.path.join('../ob-clark', 'ob-clark-bmi-' + str(i) + '.json'), 'w') as f:
            print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)

def gen_hist():
    h = familymemberhistory.FamilyMemberHistory()
    h.patient = {"reference": patient_id_ref, "display": patient_name}
    h.status = 'completed'
    h.relationship = {"coding": [{"code": "MTH", "system": "http://hl7.org/fhir/familial-relationship"}]}
    measurement = quantity.Quantity()
    measurement.unit = "cm"
    measurement.value = 162
    h.extension = [{"url": "http://fhir-registry.smarthealthit.org/StructureDefinition/family-history#height",
                    "valueQuantity": {"unit": "cm", "value": 162}}]
    with open(os.path.join('../ob-clark', 'ob-clark-mth.json'), 'w') as f:
        print(json.dumps(OrderedDict(h.as_json()), indent=4, separators=(',', ': ')), file=f)

    h = familymemberhistory.FamilyMemberHistory()
    h.patient = {"reference": patient_id_ref, "display": patient_name}
    h.status = 'completed'
    h.relationship = {"coding": [{"code": "FTH", "system": "http://hl7.org/fhir/familial-relationship"}]}
    measurement = quantity.Quantity()
    measurement.unit = "cm"
    measurement.value = 177
    h.extension = [{"url": "http://fhir-registry.smarthealthit.org/StructureDefinition/family-history#height",
                    "valueQuantity": {"unit": "cm", "value": 177}}]
    with open(os.path.join('../ob-clark', 'ob-clark-fth.json'), 'w') as f:
        print(json.dumps(OrderedDict(h.as_json()), indent=4, separators=(',', ': ')), file=f)

def gen_rel():
    r = relatedperson.RelatedPerson()
    r.patient = {"reference":patient_id_ref, "display":patient_name}
    r.relationship = {"coding":[{"code": "MTH","system":"http://hl7.org/fhir/v3/RoleCode","display":"mother"}]}
    r.name = kent_mom_name
    r.telecom = kent_telecom
    r.address = kent_address
    r.gender = "female"
    r.birthDate = str(kent_mom_dob.date())
    with open(os.path.join('../ob-clark', 'rp-clark-mth.json'),'w') as f:
        print(json.dumps(OrderedDict(r.as_json()), indent=4, separators=(',', ': ')), file=f)

    r = relatedperson.RelatedPerson()
    r.patient = {"reference":patient_id_ref, "display":patient_name}
    r.relationship = {"coding":[{"code": "SIB","system":"http://hl7.org/fhir/v3/RoleCode","display":"sibling"}]}
    r.name = kent_kara_name
    r.telecom = kent_telecom
    r.address = kent_address
    r.gender = "female"
    r.birthDate = str(kent_kara_dob.date())
    with open(os.path.join('../ob-clark', 'rp-clark-sib.json'),'w') as f:
        print(json.dumps(OrderedDict(r.as_json()), indent=4, separators=(',', ': ')), file=f)


def main():
    gen_obs()
    gen_hist()
    gen_rel()



if __name__ == '__main__':
    main()


