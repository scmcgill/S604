from pymarc import MARCReader

with open('gardensofmoonboo00erik_marc.xml', 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
        print(record.title)

