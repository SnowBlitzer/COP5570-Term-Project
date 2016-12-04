import os, sys, concurrent.futures
# from pymongo import MongoClient
# from pymongo.errors import DuplicateKeyError
from collections import Counter
from db_client import DB_Driver

# # Init db connection
# client = MongoClient()
# db = client['spam-db']
# spams = db.spams
# spams.create_index("filename", unique=True)
#
# inserts = 0
# fails = 0
# duplicates = 0
# updates = 0
# matches = 0
# errors = Counter()

year = None


def clean_line(lineHandedIn):
	"""
	Function strips all unneeded characters away and
	hands back a unique set of all words greater than
	2 Characters
	"""
	charactersToBeStripped = ".,;<>:[]\"|"
	uniqueSet = set()
	wordCount = Counter()
	for word in lineHandedIn:
		charStrippedText = word.strip(charactersToBeStripped)
		if len(charStrippedText) > 2 and charStrippedText.isalpha():
			uniqueSet.add(charStrippedText)
			wordCount[charStrippedText] += 1
	return uniqueSet, wordCount

def filter_data(item):
	if type(item) is set and len(item) is not 0:
		filtered_results.append(item)

def analyze_file(file_path):
	"""
	Handles a single file path.
	"""

	db = DB_Driver()

	# global spams
	content = set()
	word_count = Counter()
	email = None

	with open(file_path,"r") as file_contents:
		add_flag = False
		#Iterate through file contents
		for line in file_contents:
			line_tokens = line.split()

			if len(line_tokens) > 1:
				#if the flag is set, clean up all the data.
				#Discard links and strip characters. Add it to the list
				if add_flag:
					new_content, new_count = clean_line(line_tokens)
					content = content.union(new_content)
					word_count += new_count
				#Add the email to the hash table (counter)
				elif line_tokens[0] == "From:":
					email = line_tokens[-1]
				#If the content is plain/text, set the add_flag
				elif line_tokens[1] == "text/plain" or line_tokens[1] == "text/plain;":
					add_flag = True
			elif len(line_tokens) == 1 and add_flag and not line_tokens[0].isalnum():
				add_flag = False
				break

		# Format data for Mongo
		document = {
			"email":email,
			"words":list(content),
			"wordCount":word_count,
			"filename":file_path.split("/")[-1],
			"year": year
		}

		db.insert_document(document)

	return db.results, db.errors


def parse_files(files, file_year = None):
	"""
	Extracts content from list of files.
	"""

	global year
	year = file_year
	results = Counter()
	errors = Counter()

	db = DB_Driver()
	count_before = db.spams.count()

	print "There are currently %i stored records." % count_before
	print "Preparing to process %i files." % len(files)

	#dispatch
	executor = concurrent.futures.ProcessPoolExecutor(10)
	futures = [executor.submit(analyze_file, filename) for filename in files]

	# get results
	for f in concurrent.futures.as_completed(futures):
		r,e = f.result()
		results += r
		errors += e

	# for filename in files:
	# 	r,e = analyze_file(filename)
	# 	results += r
	# 	errors += e


	count_after = db.spams.count()
	print "There are now %i stored records." % db.spams.count()

	inserts = results['inserts']
	fails = results['fails']
	duplicates = results['duplicates']
	updates = results['updates']
	matches = results['matches']



	print "There were %i new inserts." % inserts
	print "There were {0} duplicate documents, {1} of which were found and {2} patched.".format(duplicates, matches, updates)

	print "There were %i failures." % fails
	if len(errors) > 0:
		print errors


if __name__ == '__main__':
	print "This script only contains functions, please use driver.py."
