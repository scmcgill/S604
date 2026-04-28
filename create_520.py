import requests
import json
import re
from pymarc import MARCReader, Record, Field, Subfield, Indicators
import get_work

def create_520(work_id):
    description = get_work.get_description(work_id)
    print(description)
    

record = Record()
record.add_field(
    Field(
        tag = '520',
        indicators = Indicators('',''),
        subfields = [
            Subfield(code='a', value=description),
        ]))
