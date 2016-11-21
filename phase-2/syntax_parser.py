import enchant
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

dict = enchant.Dict("en_US")

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

for message in spams.find():
	wordList = []
	nonWordList = []
	
	#cycles through dictionary of words
	for word in message['wordCount']:
		if(dict.check(word)):
			wordList.append(word)
		else:
			nonWordList.append(word)
	
	#adds lists of words and non words to DB
	spams.update_one(
		{
			'filename': message['filename']
		},
		{
			"$set": {
				"englishWords": wordList,
				"nonEnglishWords": nonWordList
			}
		}
	)

		
	#for printing during testing
	#print "------Words:--------\n"
	#print message['englishWords']

	#print "------Not Words:--------\n"
	#print message['nonEnglishWords']

