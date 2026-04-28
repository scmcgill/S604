from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators
import re
import get_authors

#def check_nonfiling_characters(title):
#	indef_article = "^[aA] "
#	def_article = "^[tT]he "
#	nonfiling_a = re.search(indef_article, title)
#	nonfiling_the = re.search(def_article, title)
#
#	if (nonfiling_a or nonfiling_the):
#		return True
#	else:
#		return False

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

#def move_nonfiling_characters(title):
#	# find and move nonfiling characters and format title
#	indef_article = "^[aA] "
#	def_article = "^[tT]he "
#	nonfiling_a = re.search(indef_article, title)
#	nonfiling_the = re.search(def_article, title)
#	print(nonfiling_a)
#	print(type(indef_article))
#	if nonfiling_a:
#		title = re.sub(indef_article, "", title)
#		title = "{}, A".format(title).title()
#	elif nonfiling_the:
#		title = re.sub(def_article, "", title)
#		title = "{}, The".format(title).title()
#	else:
#		title = title.title()
#	return title

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
