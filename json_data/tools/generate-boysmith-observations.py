from __future__ import print_function
import json
from collections import OrderedDict
from fhirclient.models import fhirdate, observation
from observation_commons import *
import datetime

# data for generation (provided by Aly)
# Boy Smith 2-5 yr
# Visit    Age(mos)   Wt(lbs)  Ht(in)  BMI(kg/m2)
observation_list = [
    ["MD",  24, 30, 34.5, 17.7],
    ["WIC", 24, 30, 34.5, 17.7],
    ["WIC", 30, 34, 36.25, 18],
    ["WIC", 36, 36, 38, 17.5],
    ["MD",  39, 38, 38.25, 18],
    ["WIC", 48, 44, 40, 19],
    ["MD",  51, 44, 40, 19],
    ["WIC", 52, 44, 40, 19],
    ["WIC", 54, 46, 40.25, 19.9],
    ["WIC", 57, 46.5, 40.5, 19.9],
    ["WIC", 60, 48, 42, 19.1],
]

if __name__ == '__main__':
    # set up observation structure from model
    for i in range(len(observation_list)):
        o = observation.Observation()
        o.status = 'final'
        o.code = code_root
        # add subject, encounter, effectiveDateTime, performer ?
        performer, age_mos, wt_lbs, ht_in, bmi = observation_list[i]
        o.component=[
            {"code":coding_weight, "valueQuantity": {"value":wt_lbs,"unit":"lb_av"}},
            {"code":coding_height, "valuequantity": {"value":ht_in,"unit":"in_i"}},
            {"code":coding_bmi,"valueQuantity": {"value":bmi,"unit":"kg/m2"}},
            ]
        with open('ob-clark-'+str(i)+'.json','w') as f:
            print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)
