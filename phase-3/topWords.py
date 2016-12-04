from collections import Counter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

wordCounter = Counter()

for message in spams.find():

	for word in message['nonEnglishWords']:

		wordCounter[word] += 1



for word in wordCounter.most_common(100):
	print "Word: "+ str(word)
