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
			'User-Agent':'ol2koha/0.1 (seancmcgill@proton.me)'
			}
	url = "https://openlibrary.org/api/books"
	resp = requests.get(url, params = params)
	if resp.status_code == 200:
		#print(resp.json())
		#print(resp.content)
		return resp.json()
	else:
		print(f'API error: {resp.status_code}')

def get_book_number(isbn):
	# get Open Library book identifier from search response
	key = json.dumps(ol_search(isbn).get(isbn,{}).get('key'))
	book_number = key.replace("/books/", "").replace('"', '')
	#print(f"key: {key}")
	#print(f"book number: {book_number}")
	return book_number

def get_book_data(isbn):
	book_number = get_book_number(isbn).upper()
	#print(book_number)
	url = f"https://openlibrary.org/books/{book_number}.json"
	params = {
			'format': 'json',
			'jscmd': 'data',
			'User-Agent':'ol2koha/0.1 (seancmcgill@proton.me)'
			}
	response_book = requests.get(url, params=params)
	#print(response_book.status_code)
	book_data = response_book.json()
	#print(f"book data: {book_data}")
	if response_book.status_code  == 200:
		return book_data
	else:
		print(response_book.status_code)

def get_source_records(book_data): 
	source_records = book_data["source_records"]
	#print(source_records)
	return source_records

def get_marc_urls(book_data):
	# Use book identifier to find book info and extract links to MARC records
	source_records = book_data["source_records"]
	#source_records = get_source_records(book_data)
	marc_urls = []
	for record in source_records:
		if "ia:" in record:
			record = re.sub("^ia:", "", record)
			marc_urls.append(f'https://archive.org/download/{record}/{record}_meta.mrc')
		elif "marc:" in record:
			record = re.sub("marc:", "", record)
			marc_urls.append(f'https://openlibrary.org/show-records/{record}?format=raw')
	#	print(record)
	# return list of URLs
	#print(f'MARC URLs: {marc_urls}')
	return marc_urls

def select_record(marc_urls, isbn):
	#marc_urls = get_marc_urls(book_data)
	# Iterate through list of links to MARC records and select record in order of preference: Internet Archive, LOC. 
	link = ""
	filename = ""
	# search for IA link
	ia = [i for i in marc_urls if "archive.org" in i]
	#print(marc_urls)
	#print(ia)
	loc = [i for i in marc_urls if "marc_loc" in i]

	if len(ia) > 0:
		#filename = "{}.mrc".format(filename)
		filename = f"{isbn}_internet_archive.mrc"
		link = ia[0]
	elif len(loc) > 0:
		#filename = "{}.mrc".format(filename)
		filename = f"{isbn}_loc.mrc"
		link = loc[0]

	download_data = {
		"link" : link,
		"filename" : filename
			}
	return download_data

def download_marc(link, filename):
	# Download MARC record
	resp = requests.get(link).content
	# convert response to pymarc Record()
	record = Record(resp)
	print(record.title)
	# Declare filepaths
	directory = "Records"
	filepath_marc = os.path.join(directory, filename)
	
	writer = MARCWriter(open(filepath_marc,'wb'))
	writer.write(record)
	writer.close()

	#filepath_json = re.sub(".mrc", ".json", filepath_marc)
	#with open(filepath_marc, "rb") as f:
		#try:
			#reader = MARCReader(f)
			#rec = next(reader).as_dict()
			#print(rec)
			#f.write(rec.as_dict())
			#f.close()
		#except Exception as e:
			#print(str(e))
