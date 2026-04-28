from pymarc import  MARCReader, Record, Field, Subfield, Indicators, XMLWriter
import create_245
import create_520

def create_Record(book_data):
	work_id = book_data['works'][0]['key']

	record = Record()

	field_245 = create_245.create_245(book_data)
	record.add_field(field_245)
	field_520 = create_520.create_520(work_id)
	record.add_field(field_520)
	
	file = f"{book_data['isbn_13'][0]}.mrc"
	with open(file, 'wb') as out:
		out.write(record.as_marc())
	return record
