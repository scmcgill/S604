from pymarc import MARCReader, MARCWriter, Field, Subfield
import re
import os

def remove_9XX():
	# Get list of files
	dir_list = os.listdir("./Records")
	for file in dir_list:
		# only include MARC 
		if ".mrc" in file:
			filepath = f"./Records/{file}"
			# Read MARC record from file
			with open(filepath, 'rb') as fh:
				reader = MARCReader(fh)
				pattern = "^9.*"
				# Read fields from record
				for record in reader:
					d = record.as_dict()['fields']
					for keys in d:
						for key in keys:
							# Search for 9XX fields for local data
							if re.match(pattern, key):
								# remove 9XX fields
								record.remove_fields(key)
								# Write edited record back to file
								writer = MARCWriter(open(filepath,'wb'))
								writer.write(record)
								writer.close()
				reader.close()
