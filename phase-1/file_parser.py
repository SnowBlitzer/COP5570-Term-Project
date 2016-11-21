import os, sys, concurrent.futures, codecs
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from collections import Counter

# Init db connection
client = MongoClient()
db = client['spam-db']
spams = db.spams
spams.create_index("filename", unique=True)

inserts = 0
fails = 0
duplicates = 0
updates = 0
matches = 0
errors = Counter()
 
def find_decoding(decodingWord):
	return decodingWord.strip("\"")

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

	global spams
	content = set()
	word_count = Counter()
	email = None
	character_encoding = None

	with open(file_path,"r") as file_contents:
		add_flag = False
		seven_encoded = False
		#Iterate through file contents
		for line in file_contents:
			if character_encoding != None:
				line = codecs.decode(line, character_encoding)
			line_tokens = line.split()

			if len(line_tokens) > 1:
				
				#Finds the encoding for the file content
				if line_tokens[-1][0:7] == "charset":
					character_encoding = find_decoding(line_tokens[8:])
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
				#If The content is encoded in 7bit, set the seven_encoded flag
				
			elif len(line_tokens) == 1 and add_flag and not line_tokens[0].isalnum():
				add_flag = False
				break

		# Format data for Mongo
		document = {
			"email":email,
			"words":list(content),
			"wordCount":word_count,
			"filename":file_path.split("/")[-1],
			#"raw":str(open(file_path,"r").read())
		}

		global inserts
		global fails
		global errors
		global duplicates
		global updates
		global matches

		# Attempt insert to Mongo
		try:
			spam_id = spams.insert_one(document)
			if spam_id is not None:
				inserts += 1

		except DuplicateKeyError:
			duplicates += 1

			try:
				result = spams.update_one(
					{
						'filename': document['filename']
					},
					{
						"$set": {
							"email": document['email'],
							"wordCount": document['wordCount'],
							"words": document['words']
						}
					}
				)
				matches += result.matched_count
				updates += result.modified_count
			except Exception as e:
				print e

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

	global inserts
	global fails
	global errors
	global duplicates
	global updates
	global matches

	print "There were %i new inserts." % inserts
	print "There were {0} duplicate documents, {1} of which were found and {2} patched.".format(duplicates, matches, updates)

	print "There were %i failures." % fails
	if len(errors) > 0:
		print errors


if __name__ == '__main__':
	print "This script only contains functions, please use driver.py."
