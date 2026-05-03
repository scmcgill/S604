from pymarc import  MARCReader, Record, Field, Subfield, Indicators
import re

def create_041(book_data):
	# get languages
	languages = book_data['languages']

	#retrieve language code
	language_codes = []
	for lang in languages:
		lang = re.sub('/languages/', '', lang['key'])
		language_codes.append(lang)

	# See if a translated language is listed and determine indicator 1 
	if 'translated_from' in book_data:
		indic = Indicators('1',' ')
	else:
		indic = Indicators('0',' ')
		
    # Define field
	field_041 = Field(
		tag = '041',
		indicators = indic,
		subfields = [
			]
			)
	# Create subfield(s) a for language
	for lang in language_codes:
		field_041.add_subfield('a', lang)
	# Check for original language and add subfield h if one exists
	if 'translated_from' in book_data:
		translated_from = re.sub('languages/', '', book_data['translated_from'][0]['key'])
		field_041.add_subfield('h', translated_from)

	return field_041
