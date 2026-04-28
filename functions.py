import requests
import json
import re
import time
from pymarc import MARCReader
from pymarc import Record, Field, Subfield, Indicators
import create_245

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
    print(response_book.status_code)
    book_data = response_book.json()
    #print(f"book data: {book_data}")
    if response_book.status_code  == 200:
        return book_data
    else:
        print(response_book.status_code)

def get_source_records(book_data): 
    source_records = book_data.get("source_records")
    #print(source_records)
    return source_records

def get_marc_urls(book_data):
    # Use book identifier to find book info and extract links to MARC records
    source_records = get_source_records(book_data)
    marc_urls = []
    for record in source_records:
        if "ia:" in record:
            record = re.sub("^ia:", "", record)
            marc_urls.append(f'https://archive.org/download/{record}/{record}_meta.mrc')
        elif "marc:" in record:
            record = re.sub("marc:", "", record)
            marc_urls.append(f'https://openlibrary.org/show-records/{record}?format=raw')
    #    print(record)
    # return list of URLs
    #print(f'MARC URLs: {marc_urls}')
    return marc_urls

def download_marc(book_data):
    marc_urls = get_marc_urls(book_data)
    file_names = []
    try:
        for link in marc_urls :
            if "openlibrary.org" in link:
                filename = link.replace("https://openlibrary.org/show-records/", "").replace("/","-").replace(".","-").replace("?format=raw","")
                filename = "{}.mrc".format(filename)
            elif "archive.org" in link:
                filename = re.sub("https://archive.org/download/.*/", "", link).replace("?format=raw","")
                filename = "{}.mrc".format(filename)
            else:
                continue
            file_names.append(filename)
        print(f"File names\n{file_names}")
        print(f"URLs\n{marc_urls}")
                #create_marc(isbn)
        
        for file in file_names:

            with open(f"{file}", "wb") as f:
                record = requests.get(link).content
                f.write(record)
    except IndexError:
        print(f"Index error. Is the list empty? {marc_urls}")

def get_author(author_id):
    params = {
            'format': 'json',
            'jscmd': 'data',
            'User-Agent':'ol2koha/0.1 (seancmcgill@proton.me)'
            }
    #author_name = requests.get("https://openlibrary.org{author_id}.json", params=params).content["authors"][0]
    print(f"https://openlibrary.org{author_id}.json")


def test_245():
    create_245.create_245(get_book_data("0246138815"))
