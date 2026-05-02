import requests
import json
import re
from pymarc import MARCReader, Record, Field, Subfield, Indicators
import get_work


def create_520(work_id):
	# check for description notes in work data
	if get_work.get_description(work_id):
		description = get_work.get_description(work_id)
		# Add field 520 (summary notes) with description from data
		field_520 = Field(
			tag = '520',
			indicators = Indicators('',''),
			subfields = [
				Subfield(code='a', value=description),
			])
		return field_520
