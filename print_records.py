import os
from pymarc import MARCReader

def print_records():
	dir_list = os.listdir("./Records")
	for file in dir_list:
		if ".mrc" in file:
			filepath = f"./Records/{file}"
			with open(filepath, "rb") as fh:
				reader = MARCReader(fh)
				for record in reader:
					print(f"{filepath}:")
					print(record)
					print()
