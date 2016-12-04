from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

smallMessageCount = 0.0
mediumMessageCount = 0.0
largeMessageCount = 0.0
smallWrongWordCount = 0.0
mediumWrongWordCount = 0.0
largeWrongWordCount = 0.0

for message in spams.find():

	wordCount = len(message['englishWords']) + len(message['nonEnglishWords'])

	if wordCount < 20 and wordCount > 0:
		smallMessageCount += 1
		smallWrongWordCount += len(message['nonEnglishWords'])


	elif wordCount < 50 and wordCount > 0:
		mediumMessageCount += 1
		mediumWrongWordCount += len(message['nonEnglishWords'])


	elif wordCount < 100 and wordCount > 0:
		largeMessageCount += 1
		largeWrongWordCount += len(message['nonEnglishWords'])


print "Small: " + str(smallWrongWordCount/smallMessageCount)

print "Medium: " + str(mediumWrongWordCount/mediumMessageCount)

print "Large: " + str(largeWrongWordCount/largeMessageCount)
with open("errorByLenData","w") as out_file:
	out_file.write("small," + str(smallWrongWordCount/smallMessageCount)+","			"medium,"+str(mediumWrongWordCount/mediumMessageCount)+","
			"large,"+str(largeWrongWordCount/largeMessageCount))
			
