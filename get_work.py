import requests
import json
import re
import time
from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators

# Retrieve json data about author file based on author ID from edition data
def get_work_data(work_id):
	url = f"https://openlibrary.org{work_id}.json"

	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent':'ol2koha/0.1 (seancmcgill@proton.me)'
			}
	resp = requests.get(url, params = params)
	if resp.status_code == 200:
		return resp.json()

def get_description(work_id):
	work_data = get_work_data(work_id)
	if 'description' in work_data:
		description = work_data['description']
		# sometime the description has 'type' and 'value' subfields: check for 'value' subfield and use as description if it exists
		if 'value' in work_data['description']:
			description = description['value']
		return description
	else:
		pass

#print(get_description('/works/OL5734756W'))
