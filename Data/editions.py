import requests
import json
import re
from pymarc import MARCReader, MARCWriter, Record, Field, Subfield, Indicators
import os

def ol_search(isbn):
	# search API by ISBN
	params = {
			'bibkeys': isbn,
			'format': 'json',
			'jscmd': 'data',
			'User-Agent':'ol2marc/0.1 (seancmcgill@proton.me)'
			}
	url = "https://openlibrary.org/api/books"
	resp = requests.get(url, params = params)
	if resp.status_code == 200:
		# Return search data
		return resp.json()
	else:
		print(f'API error: {resp.status_code}')

def get_book_number(isbn):
	# get Open Library edition identifier from search response
	key = json.dumps(ol_search(isbn).get(isbn,{}).get('key'))
	book_number = key.replace("/books/", "").replace('"', '')
	return book_number

def get_book_data(isbn):
	# Get edition data 
	book_number = get_book_number(isbn).upper()
	url = f"https://openlibrary.org/books/{book_number}.json"
	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent':'ol2marc/0.1 (seancmcgill@proton.me)'
			}
	response_book = requests.get(url, params=params)
	book_data = response_book.json()
	if response_book.status_code  == 200:
		return book_data
	else:
		print(response_book.status_code)

def get_source_records(book_data): 
	# Get a list of available MARC records
	source_records = book_data["source_records"]
	return source_records

def get_marc_urls(book_data):
	# Get a list of identifiers for this edition's MARC records
	if 'source_records' in book_data:
		source_records = book_data["source_records"]
		marc_urls = []
		for record in source_records:
			# Create download link from source record identifier
			if "ia:" in record:
				record = re.sub("^ia:", "", record)
				marc_urls.append(f'https://archive.org/download/{record}/{record}_meta.mrc')
			elif "marc:" in record:
				record = re.sub("marc:", "", record)
				marc_urls.append(f'https://openlibrary.org/show-records/{record}?format=raw')
		# return list of URLs for downloadable records
		return marc_urls

def select_record(marc_urls, isbn):
	# Iterate through list of links to MARC records and select record in order of preference: LOC, Internet Archive. Return empty dictionary if neither source available
	link = ""
	filename = ""
	# search for IA link
	ia = [i for i in marc_urls if "archive.org" in i]
	# search for LOC link
	loc = [i for i in marc_urls if "marc_loc" in i]

	# Select LOC record or Internet Archive record
	if loc and len(loc) > 0:
		filename = f"{isbn}_loc.mrc"
		link = loc[0]
	elif ia and len(ia) > 0:
		filename = f"{isbn}_internet_archive.mrc"
		link = ia[0]

	download_data = {
		"link" : link,
		"filename" : filename
			}
	# Return dictionary with download link and file name
	return download_data

def download_marc(link, filename):
	# Download MARC record
	resp = requests.get(link).content
	# convert response to pymarc Record()
	record = Record(resp)
	# Declare filepath
	directory = "Records"
	filepath = os.path.join(directory, filename)
	# Write Pymarc record to file	
	writer = MARCWriter(open(filepath,'wb'))
	writer.write(record)
	writer.close()
