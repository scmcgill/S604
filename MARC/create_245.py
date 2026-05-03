from pymarc import MARCReader, Record, Field, Subfield, Indicators
import re
from Data import get_authors

def count_nonfiling_characters(title):
	# Find number of nonfiling characters (articles, spaces) at the front of the title
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
	except:
		pass
	try:
		# get edition title
		title = book_data["title"]
	except:
		title = " "

	# subtitle data
	try:
		subtitle = book_data["subtitle"]
	except:
		subtitle = ""

	# Check for statement of responsibility in edition data
	if 'by_statement' in book_data:
			responsibility = book_data['by_statement']
	else:
			# If no statement of responsibility in data, add it
		responsibility = f"by {get_authors.get_author_name(author_key)['fn_ln']}"

# create MARC record and field 245
	# Define field 245
	field_245 =	Field(
			tag = '245',
			# Write number of nonfiling characters
			indicators = Indicators('0', count_nonfiling_characters(title)),
			subfields = [
				# Add subfields for title, subtitle, statement of responsibility
				Subfield(code='a', value=title),
				Subfield(code='b', value=subtitle),
				Subfield(code='c', value=responsibility)
			]) 
	
	return field_245
