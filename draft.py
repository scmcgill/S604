import time
import editions
import create_MARC

# get list of isbns from file
with open('isbns.txt', 'r') as f:
	isbns = [str(line.strip()) for line in f]
print(isbns)

def bulk_download_marc(isbns):
	for isbn in isbns:
		# get edition data from API by searching isbn
		book_data = editions.get_book_data(isbn)
		# Get urls of records for this edition
		if editions.get_marc_urls(book_data):
			marc_urls = editions.get_marc_urls(book_data)
		# Select Inernet Archive or LOC records, if available.  Return dictionary with empty values if not.
			if editions.select_record(marc_urls, isbn):
				download_data = editions.select_record(marc_urls, isbn)
			# check if IA or LOC record is available, then download one of them
			if download_data["link"] != "" and download_data["filename"] != "":
				editions.download_marc(download_data["link"],download_data["filename"])
		else:
			# Create basic MARC record from Open Library data
			create_MARC.create_Record(isbn)
		# Pause loop to avoid having requests denied
		time.sleep(5)

bulk_download_marc(isbns)
