from pymarc import  MARCReader, Record, Field, Subfield, Indicators, XMLWriter
import create_041
import create_100
import create_245
import create_520
import editions
import os

def create_Record(isbn):
	book_data = editions.get_book_data(isbn)
	work_id = book_data['works'][0]['key']
	author_id = book_data['authors'][0]['key']
	record = Record()
	
	field_041 = create_041.create_041(book_data)
	record.add_field(field_041)
	field_100 = create_100.create_100(author_id)
	record.add_field(field_100)
	field_245 = create_245.create_245(book_data)
	record.add_field(field_245)
	field_520 = create_520.create_520(work_id)
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
