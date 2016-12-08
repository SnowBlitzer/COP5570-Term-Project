import os, sys, concurrent.futures
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from collections import Counter
from db_client import DB_Driver

# # Init db connection
client = MongoClient()
db = client['spam-db']
control = db.control

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
	Handles a single pre-existing document.
	"""

	content = set()
	word_count = Counter()
	email = None

	#Iterate through file contents
	#for line in messageIn['body']:
	line_tokens = messageIn['body'].split()

	if len(line_tokens) > 1:
		#Discard links and strip characters. Add it to the list
		new_content, new_count = clean_line(line_tokens)
		content = content.union(new_content)
		word_count += new_count

	# Add our fields
	control.update_one(
		{
			'_id': messageIn['_id']
		},
		{
			"$set":{
				"email":messageIn['headers']['From'],
				"words":list(content),
				"wordCount":word_count,
				"year": messageIn['headers']['Date'].split()[3],
				"version":1
			}
		}
	)


def parse_documents():
	"""
	Extracts content from list of files.
	"""

	count_before = control.find().count()

	print "There are currently %i unprocessed records." % count_before

	#dispatch
	# executor = concurrent.futures.ThreadPoolExecutor(10)
	# futures = [executor.submit(analyze_message, document) for document in control.find()]
	# concurrent.futures.wait(futures)

	for document in control.find():
		analyze_message(document)

	count_after = control.count()
	print "There are now %i stored records." % control.count()


if __name__ == '__main__':
	parse_documents()
