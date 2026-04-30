import pymarc
from pymarc import  MARCReader, Record, Field, Subfield, Indicators, XMLWriter
import create_041
import create_100
import create_245
import create_520

def create_Record(book_data):
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
	
	if 'isbn_10' in book_data:
		isbn = book_data['isbn_10'][0]
		
	file = f"{isbn}.mrc"
	with open(file, 'wb') as out:
		out.write(record.as_marc21())
	record_dict = record.as_dict()
	print(record_dict)
	return record
