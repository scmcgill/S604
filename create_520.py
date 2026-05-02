import requests
import json
import re
from pymarc import MARCReader, Record, Field, Subfield, Indicators
import get_work


def create_520(work_id):
	if get_work.get_description(work_id):
		description = get_work.get_description(work_id)
		field_520 = Field(
			tag = '520',
			indicators = Indicators('',''),
			subfields = [
				Subfield(code='a', value=description),
			])
		#print(field_520)
		return field_520
