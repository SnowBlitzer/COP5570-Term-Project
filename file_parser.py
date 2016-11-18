import os, sys, concurrent.futures

# Global data structures
emails = dict()
parse_results = list()
filtered_results = list()

def clean_line(lineHandedIn):
	"""
	Function strips all unneeded characters away and
	hands back a unique set of all words greater than
	2 Characters
	"""
	charactersToBeStripped = ".,;<>:[]\"|"
	uniqueSet = set()
	for x in lineHandedIn:
		charStrippedText = x.strip(charactersToBeStripped)
		if len(charStrippedText) > 2 and charStrippedText.isalpha():
			uniqueSet.add(charStrippedText)
	return uniqueSet

def filter_data(item):
	if type(item) is set and len(item) is not 0:
		filtered_results.append(item)

def analyze_file(file_path):
	"""
	Handles a single file path.
	"""

	addFlag = False
	content = set()
	global parse_results
	global emails

	with open(file_path,"r") as file_contents:
		#Iterate through file contents
		for line in file_contents:
			line_tokens = line.split()

			if len(line_tokens) > 1:
				#if the flag is set, clean up all the data.
				#Discard links and strip characters. Add it to the list
				if addFlag:
					content = content.union(clean_line(line_tokens))
				#Add the email to the hash table (counter)
				elif line_tokens[0] == "From:":
					if line_tokens[-1] in emails:
						emails[line_tokens[-1]] += 1
					else:
						emails[line_tokens[-1]] = 1
				#If the content is plain/text, set the addFlag
				elif line_tokens[1] == "text/plain" or line_tokens[1] == "text/plain;":
					addFlag = True
			elif len(line_tokens) == 1 and addFlag and not line_tokens[0].isalnum():
				addFlag = False
				break
		parse_results.append(content)

def parse_files(files):
	"""
	Extracts content from list of files.
	"""

	# code from stack_overflow
	executor = concurrent.futures.ThreadPoolExecutor(10)
	futures = [executor.submit(analyze_file, filename) for filename in files]
	concurrent.futures.wait(futures)


	global parse_results

	filtered_results = [item for item in parse_results if len(item) is not 0]


	# clean dataset
	# executor = concurrent.futures.ThreadPoolExecutor(10)
	# futures = [executor.submit(filter_data, item) for item in parse_results]
	# concurrent.futures.wait(futures)

	# global filtered_results
	return filtered_results

def parse_files_single_thread(files):
	for file_path in files:
		analyze_file(file_path)
	global parse_results
	return [item for item in parse_results if len(item) is not 0]


if __name__ == '__main__':
	print "This script only contains functions, please use driver.py."
