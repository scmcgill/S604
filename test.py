import requests
import json
import re

isbn = "9780765348784"

def ol_search():
    # search API by ISBN
    params = {
            'bibkeys': isbn,
            'format': 'json',
            'jscmd': 'data',
            'User-Agent':'ol2koha/0.0 (seancmcgill@proton.me'
            }
    url = "https://openlibrary.org/api/books"
    resp = requests.get(url, params = params)
    if resp.status_code == 200:
        print(resp.json())
        return resp.json()
    else:
        print(f'API error: {resp.status_code}')

def get_book_number():
    # get Open Library book identifier from search response
    key = json.dumps(ol_search().get(isbn,{}).get('key'))
    book_number = key.replace("/books/", "").replace('"', '')
    print(book_number)
    return book_number

def get_book_data():
    book_number = get_book_number().upper()
    url = f"https://openlibrary.org/books/{book_number}.json"
    params = {
            'format': 'json',
            'jscmd': 'data'
            }
    response_book = requests.get(url, params=params)
    book_data = response_book.json()
    if response_book.status_code  == 200:
        return book_data
    else:
            print(response_book.status_code)

def get_source_records(): 
    book_data = get_book_data()
    source_records = book_data["source_records"]
    return source_records

def get_marc_urls():
    # Use book identifier to find book info and extract links to MARC records
    source_records = get_source_records()
    marc_urls = []
    for record in source_records:
        if "ia:" in record:
            record = re.sub("^ia:", "", record)
            marc_urls.append(f'https://archive.org/download/{record}/{record}_marc.xml')
            print(record)
        elif "marc:" in record:
            record = re.sub("marc:", "", record)
            marc_urls.append(f'https://openlibrary.org/show-records/{record}?format=xml')
    # return list of URLs
    print(f'MARC URLs: {marc_urls}')
    return marc_urls

def download_marc():
    marc_urls = get_marc_urls()
    try:
        for link in marc_urls :
            if "openlibrary.org" in link:
                filename = link.replace("https://openlibrary.org/show-records/", "").replace("/","-").replace(".","-").replace("?format=xml", "")
            elif "archive.org" in link:
                filename = re.sub("https://archive.org/download/.*/", "", link)
                print(filename)
        with open(f"{filename}", "wb") as f:
            record = requests.get(link).content
            f.write(record)
    except IndexError:
        print(f"Index error. Is the list empty? {marc_urls}")

download_marc()
#print(get_marc_urls())
# need to switch formats to raw MARC to facilitate pymarc import. Or figure out how to import marcxml to raw marc?
