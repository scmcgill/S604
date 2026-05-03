from pymarc import  MARCReader, Record, Field, Subfield, Indicators, XMLWriter
import create_041
import create_100
import create_245
import create_520
import get_work
import editions
import os
import requests

def create_Record(isbn):
	# Get edition data
	book_data = editions.get_book_data(isbn)
	# Get work id from edition data and download work data
	work_id = book_data['works'][0]['key']
	work_data = get_work.get_work_data(work_id)
	# Get auhtor id from work data and download author data
	author_id = work_data['authors'][0]['author']['key']
	# Define record and add subfields
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
	
	# Define file names and paths
	directory = "./Records"
	filename_marc = f"{isbn}_OL_data.mrc"
	filepath_marc = os.path.join(directory, filename_marc)

	# Write record to file
	with open(filepath_marc, 'wb') as out:
		out.write(record.as_marc())
