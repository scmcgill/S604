from pymarc import  MARCReader, Record, Field, Subfield, Indicators
from Data import get_authors

def create_100(author_id):
	# Get author name by requesting author data from Open Library
	author_name = get_authors.get_author_name(author_id)

    # Define Field
	field_100 = Field(
		tag = '100',
		indicators = Indicators('1',' '),
		subfields = [
            # Add author's name from dictionary returned by get_author_name
			Subfield(code='a', value=author_name['ln_fn'])
			]
			)
	return field_100
