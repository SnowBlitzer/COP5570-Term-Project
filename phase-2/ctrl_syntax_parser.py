import enchant
import concurrent.futures
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import sys

edict = enchant.DictWithPWL("en_US", "mywords.txt")
fdict = enchant.Dict("fr_FR")

def get_client():
	client = MongoClient()    # Open client connection
	db = client['spam-db']    # choose database
	control = db.control          # this is our collection
	return control

def process_message(message):
	wordList = []
	nonWordList = []

	#cycles through dictionary of words
	for word in message['wordCount']:
		if(edict.check(word) or fdict.check(word)):
			wordList.append(word)
		else:
			nonWordList.append(word)


	db = get_client()
	#adds lists of words and non words to DB
	db.update_one(
		{
			'_id': message['_id']
		},
		{
			"$set": {
				"englishWords": wordList,
				"nonEnglishWords": nonWordList,
				"version":3
			}
		}
	)

def process_year(year):

	ok = 0
	nope = 0

	db = get_client()
	documents = db.find({"year":year, "version":{'$lt':3}})
	print "There are {0} unprocessed documents in year {1}".format(documents.count(), year)
	for document in documents:
		try:
			process_message(document)
			ok+=1
		except:
			nope+=1

	print "For year {0}, we had {1} ok and {2} fails".format(year, ok, nope)


if __name__ == "__main__":

	db = get_client()

	# figure out how many years we have
	years = db.find().distinct("year")

	print years

	# executor = concurrent.futures.ProcessPoolExecutor(len(years))
	# futures = [executor.submit(process_year, year) for year in years]
	# concurrent.futures.wait(futures)

	for year in years:
		process_year(year)

	#for printing during testing
	#print "------Words:--------\n"
	#print message['englishWords']

	#print "------Not Words:--------\n"
	#print message['nonEnglishWords']
