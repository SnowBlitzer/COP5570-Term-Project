import os, sys, concurrent.futures
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from collections import Counter
from db_client import DB_Driver

# # Init db connection
client = MongoClient()
db = client['spam-db']
control = db.control
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

def analyze_message(messageIn):
	"""
	Handles a single file path.
	"""

	db = DB_Driver()

	# global spams
	content = set()
	word_count = Counter()
	email = None

	
	add_flag = False
	#Iterate through file contents
	for line in messageIn['body']:
		line_tokens = line.split()

		if len(line_tokens) > 1:
			#if the flag is set, clean up all the data.
			#Discard links and strip characters. Add it to the list
			
			new_content, new_count = clean_line(line_tokens)
			content = content.union(new_content)
			word_count += new_count

	# Format data for Mongo
	document = {
		"email":messageIn.find(headers['From']),
		"words":list(content),
		"wordCount":word_count,
		"filename":messageIn['filename'],
		"year": messageIn.find(headers['Date']).split()[3]
	}

	db.insert_document(document)

	return db.results, db.errors


def parse_files(files, file_year = None):
	"""
	Extracts content from list of files.
	"""

	global year
	#year = file_year
	results = Counter()
	errors = Counter()

	db = DB_Driver()
	count_before =0# db.control.count()

	print "There are currently %i stored records." % count_before
	print "Preparing to process %i files." % len(files)

	#dispatch
	executor = concurrent.futures.ThreadPoolExecutor(10)
	futures = [executor.submit(analyze_message, messages) for messages in control.find()]

	# get results
	for f in concurrent.futures.as_completed(futures):
		r,e = f.result()
		results += r
		errors += e

	# for filename in files:
	# 	r,e = analyze_file(filename)
	# 	results += r
	# 	errors += e


	count_after = db.control.count()
	print "There are now %i stored records." % db.control.count()

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
