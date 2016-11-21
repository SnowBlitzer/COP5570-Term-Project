import enchant
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

dict = enchant.Dict("en_US")

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

for message in spams.find():
	for word in message['words']:
		if(dict.check(word)):
			print word
		else:
			print "-----" + word

