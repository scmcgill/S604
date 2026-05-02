from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators
import re
import get_authors

def count_nonfiling_characters(title):
	indef_article = "^[aA] "
	def_article = "^[tT]he "
	nonfiling_a = re.search(indef_article, title)
	nonfiling_the = re.search(def_article, title)
	if nonfiling_a:
		return 2
	elif nonfiling_the:
		return 4
	else:
		return 0

def create_245(book_data, work_data):
	# title data
	try:
		# get OL key of first listed author
		author_key = work_data['authors'][0]['author']['key']
		print(author_key)
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
	if 'by_statement' in book_data:
			responsibility = book_data['by_statement']
	else:
			# get name of first listed author in 'Last name, First name' order
		responsibility = f"by {get_authors.get_author_name(author_key)['fn_ln']}"

	#print(author_key)
	#print(responsibility)

	# count nonfiling characters in title
	#nonfiling_characters = check_nonfiling_characters(title)

# create MARC record and field 245
	# Add field 245
	field_245 =	Field(
			tag = '245',
			indicators = Indicators('0', count_nonfiling_characters(title)),
			subfields = [
				Subfield(code='a', value=title),
				Subfield(code='b', value=subtitle),
				Subfield(code='c', value=responsibility)
			]) 
	
	#print(field_245)
	return field_245
