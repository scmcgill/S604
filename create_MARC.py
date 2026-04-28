from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators
import re
import get_authors
import create_245
import create_520


def create_245(book_data):
	# title data
	try:
		# get OL key of first listed author
		author_key = book_data['authors'][0]['key']
	except:
		pass
	try:
		title = book_data["title"]
	except:
		title = " "

	# subtitle data
	try:
		subtitle = book_data["subtitle"]
	except:
		subtitle = ""

	# statement of responsibility data
	try:
		if book_data['by_statement']:
			responsibility = book_data['by_statement']
		else:
			# get name of first listed author in 'Last name, First name' order
			responsibility = get_authors.get_author_name(author_key)['ln_fn']
	except Exception:
		responsibility = ''
		print(Exception)

#	responsibility = f"by {get_authors.get_author_name(author_key)['fn_ln']}"
	print(author_key)
	print(responsibility)

	# count nonfiling characters in title
	#nonfiling_characters = check_nonfiling_characters(title)

# create MARC record and field 245
	record = Record()
	record.add_field(
	# Add field 245
		Field(
			tag = '245',
			indicators = Indicators('0', count_nonfiling_characters(title)),
			subfields = [
				Subfield(code='a', value=title),
				Subfield(code='b', value=subtitle),
				Subfield(code='c', value=responsibility)
			])) 
	
	print(record['245'])
	#return record

