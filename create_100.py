from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators
import get_authors

def create_100(author_id):
	# Get author name by requesting author data from Open Library
	author_name = get_authors.get_author_name(author_id)

	field_100 = Field(
		tag = '100',
		indicators = Indicators('1',''),
		subfields = [
			Subfield(code='a', value=author_name['ln_fn'])
			]
			)
	return field_100
