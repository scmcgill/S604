import requests
import json
from nameparser import HumanName

# Retrieve json data about author file based on author ID from edition data
def get_author_data(author_id):
	url = f"https://openlibrary.org{author_id}.json"

	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent':'ol2koha/0.1 (seancmcgill@proton.me)'
			}
	resp = requests.get(url, params = params)
	if resp.status_code == 200:
		return resp.json()

# Get author's name from Open Library author data
def get_author_name(author_id):
	author_data = get_author_data(author_id)
	name = HumanName(author_data['name'])
	try:
		name_first = name.first
	except:
		pass
	try:
		name_last = name.last
	except:
		pass
	try:
		name_middle = name.middle
	except:
		pass
	# concatenate last/first names, removing trailing space if no middle name
	ln_fn = f"{name_last}, {name_first} {name_middle}".rstrip()
	# concatenate first/last names, removing extra space if no middle name
	fn_ln = f"{name_first} {name_middle} {name_last}".replace("  ", " ")
	# Return dictionary of names in first/last, last/first order
	author_names = {
		"ln_fn" : ln_fn,
		"fn_ln" : fn_ln
			}
	return author_names
