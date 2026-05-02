from pymarc import  MARCReader, Record, Field, Subfield, Indicators, XMLWriter
import create_041
import create_100
import create_245
import create_520
import editions
import os
import requests

def get_work_data(work_id):
	url = f"https://openlibrary.org/{work_id}.json"
	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent': 'ol2koha/0.1 (seancmcgill@proton.me)'
			}
	resp = requests.get(url, params=params)
	print(url)
	print(resp.content)
	print(resp.status_code)
	if resp.status_code == 200:
		work_data = resp.json()
		return work_data

def create_Record(isbn):
	book_data = editions.get_book_data(isbn)
	work_id = book_data['works'][0]['key']
	work_data = get_work_data(work_id)
	author_id = work_data['authors'][0]['author']['key']
	record = Record()
	if 'languages' in book_data:	
		field_041 = create_041.create_041(book_data)
		record.add_field(field_041)
	if author_id:
		field_100 = create_100.create_100(author_id)
		record.add_field(field_100)
	field_245 = create_245.create_245(book_data, work_data)
	record.add_field(field_245)
	field_520 = create_520.create_520(work_id)
	if field_520:
		record.add_field(field_520)
	
	directory = "./Records"
	filename_marc = f"{isbn}_OL_data.mrc"
	filepath_marc = os.path.join(directory, filename_marc)

	with open(filepath_marc, 'wb') as out:
		out.write(record.as_marc())

	filename_json = f"{isbn}_OL_data.json"
	filepath_json = os.path.join(directory, filename_json)

	#with open(filepath_json, 'w') as out:
		#out.write(record.as_json())
