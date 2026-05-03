import json
import time
from Data import editions
from MARC import create_MARC, remove_9XX,  print_records
import os
import traceback
import print_errors

# get list of isbns from file
with open('isbns.txt', 'r') as f:
	isbns = [str(line.strip()) for line in f]

# Download MARC records of editions relating to ISBNs
def bulk_download_marc(isbns):

	# Create directory for records if none exists
	try:
		os.mkdir("Records")
		print(f"Directory 'Records' created successfully.")
	except FileExistsError:
		print(f"Directory 'Records' already exists.")

	for isbn in isbns:
		print(f"Searching for record for {isbn}")
		try:
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
					# Download selected record
					editions.download_marc(download_data["link"],download_data["filename"])
			else:
				# Create basic MARC record from Open Library data if MARC download is not available
				print(f"No LOC or Internet Archive record available. Creating record for {isbn}")
				create_MARC.create_Record(isbn)

		except Exception as e:
			print(str(e))
			trace = traceback.format_exc()
			print_errors.print_errors(isbn, e, trace)
				  
		# Pause loop to avoid having requests denied
		time.sleep(5)
	# Remove local data from 9XX fields in MARC records
	remove_9XX.remove_9XX()

bulk_download_marc(isbns)
# Print records
#print_records.print_records()
