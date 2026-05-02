from pymarc import MARCReader, Record, Field, Subfield, Indicators

with open('9781429926584_OL_data.mrc', 'rb') as fh:
	reader = MARCReader(fh)
	print(reader)
	for record in reader:
		print(record)
	reader.close()
