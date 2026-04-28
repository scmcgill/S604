#import requests
#import json
#import re
#import time
#from pymarc import MARCReader
#from pymarc import Record, Field, Subfield, Indicators
import functions

isbn = "9780316005401"
book_data = functions.get_book_data(isbn)
print(book_data)
    
#functions.get_author("/authors/OL1394250A")
#functions.download_marc(book_data)
#print(book_data["subjects"])
#get_marc_urls(isbn)
#print("Enter ISBN or filename:")
#inp = input()
#if "." in inp:
#    file = inp
#    with open(file, "r") as f:
#        for line in f:
#            download_marc(line)
#            time.sleep(5)
#else:
#    download_marc(inp)
# Need to test on a file with multiple lines, add functionality to recognize csv files
# Editions w/o xml record are downloading the HTML of the MARC record's page.  Need to detect presence of record types.
