import requests
import json

# Get data about a work from Open Library API
def get_work_data(work_id):
	url = f"https://openlibrary.org/{work_id}.json"
	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent': 'ol2marc/0.1 (seancmcgill@proton.me)'
			}
	resp = requests.get(url, params=params)
	if resp.status_code == 200:
		work_data = resp.json()
		return work_data

# Get description of work from Open Library work data
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
