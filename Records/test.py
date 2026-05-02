from pymarc import MARCReader, Record, Field, Subfield, Indicators

with open('9780316005401_loc.mrc', 'rb') as fh:
	reader = MARCReader(fh)
	print(reader)
	for record in reader:
		print(record)
	reader.close()
