from pymarc import MARCReader, Record, Field, Subfield, Indicators

with open('9780765348784_internet_archive.mrc', 'rb') as fh:
	reader = MARCReader(fh)
	print(reader)
	for record in reader:
		print(record)
