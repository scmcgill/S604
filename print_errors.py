import json
import os
import traceback

def print_errors(isbn, error, trace):
# collect exception info
	error_data = {
		isbn : {
		"Error": str(error),
		"Traceback": str(trace)
			}
		}
	# Save error data to json file.
	if not os.path.exists("errors.json"):
		print("no errors file")
		with open("errors.json", "w") as f:
			json.dump(error_data, f)
	else:
		with open("errors.json", "r") as f:
			file_json = json.load(f)
			file_json.update(error_data)
			f.close()
		with open("errors.json", "w") as f:
			json.dump(file_json, f)
