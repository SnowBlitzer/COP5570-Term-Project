import os, sys, concurrent.futures
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from collections import Counter

# Init db connection
client = MongoClient()
db = client['spam-db']
spams = db.spams
spams.create_index("filename", unique=True)

successes = 0
fails = 0
duplicates = 0
errors = Counter()


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

	global spams
	content = set()
	email = None

	with open(file_path,"r") as file_contents:
		addFlag = False
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
					email = line_tokens[-1]
				#If the content is plain/text, set the addFlag
				elif line_tokens[1] == "text/plain" or line_tokens[1] == "text/plain;":
					addFlag = True
			elif len(line_tokens) == 1 and addFlag and not line_tokens[0].isalnum():
				addFlag = False
				break

		# Format data for Mongo
		document = {
			"email":email,
			"words":list(content),
			"filename":file_path.split("/")[-1],
			"raw":str(open(file_path,"r").read())
		}

		global successes
		global fails
		global errors

		# Attempt insert to Mongo
		try:
			spam_id = spams.insert_one(document)
			if spam_id is not None:
				successes += 1
		except DuplicateKeyError:
			duplicates += 1
		except Exception as e:
			fails += 1
			errors[type(e)] += 1




def parse_files(files):
	"""
	Extracts content from list of files.
	"""

	global spams

	count_before = spams.count()

	print "There are currently %i stored records." % count_before
	print "Preparing to process %i files." % len(files)

	# code from stack_overflow
	executor = concurrent.futures.ThreadPoolExecutor(10)
	futures = [executor.submit(analyze_file, filename) for filename in files]
	concurrent.futures.wait(futures)


	count_after = spams.count()
	print "There are now %i stored records." % spams.count()

	global successes
	global fails
	global errors
	global duplicates

	print "There were {0} successes, {1} failures, and {2} duplicates".format(successes, fails, duplicates)
	if len(errors) > 0:
		print errors


if __name__ == '__main__':
	print "This script only contains functions, please use driver.py."
