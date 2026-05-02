from pymarc import MARCReader, Record, Field, Subfield, Indicators

with open('9780553805451_loc.mrc', 'rb') as fh:
	reader = MARCReader(fh)
	print(reader)
	for record in reader:
		print(record)
	reader.close()
