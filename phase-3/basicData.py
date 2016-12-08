from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

recordCount = 0
nonEnglishRecord = 0
wrongWordCount = 0.0
correctWordCount = 0.0
totalWordCount = 0.0

for message in spams.find():
	
	recordCount += 1
	if "nonEnglishWords" in message:
		if message['nonEnglishWords']:
			nonEnglishRecord += 1

        if "englishWords" not in message:
          continue

        totalWordCount += len(message['englishWords'])
        totalWordCount += len(message['nonEnglishWords'])
        correctWordCount += len(message['englishWords'])
        wrongWordCount += len(message['nonEnglishWords'])




print "Records: " + str(recordCount)
print "Records with errors: " + str(nonEnglishRecord)
print "Words: " + str(correctWordCount)
print "Errors: " + str(wrongWordCount)
