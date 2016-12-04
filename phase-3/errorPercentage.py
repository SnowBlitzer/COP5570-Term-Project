from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

messageCount = 0
wrongWordCount = 0.0
correctWordCount = 0.0
correctWordsWithErrors = 0.0

for message in spams.find():
	
	if len(message['nonEnglishWords']) + len(message['englishWords']) > 0:
		messageCount += 1
	
	wrongWordCount += len(message['nonEnglishWords'])
	if len(message['nonEnglishWords']) > 0:
		correctWordsWithErrors += len(message['englishWords'])

	correctWordCount += len(message['englishWords'])

wrongWordCount/correctWordCount

print "Messages: " + str(messageCount)
print "Words: " + str(correctWordCount)
print "Errors: " + str(wrongWordCount)

print "Percentage: " + str(wrongWordCount/correctWordCount *100)
print "Percentage2: " + str(wrongWordCount/correctWordsWithErrors *100)
