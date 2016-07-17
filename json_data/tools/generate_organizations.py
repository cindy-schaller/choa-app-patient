from __future__ import print_function
import json
import os
from collections import OrderedDict
from fhirclient.models import organization
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():
    # create WIC organization
    o = organization.Organization()
    o.name = "WIC"
    with open('organization-wic.json','w') as f:
        print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)

    # create MD organization
    o = organization.Organization()
    o.name = "MD"
    with open('organization-md.json','w') as f:
        print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)

    # create Patient Care Coordinator organization
    o = organization.Organization()
    o.name = "Patient Care Coordinator"
    with open('organization-patco.json', 'w') as f:
        print(json.dumps(OrderedDict(o.as_json()), indent=4, separators=(',', ': ')), file=f)


if __name__ == '__main__':
    main()
