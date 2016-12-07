from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

messageCount = [ 0, 0, 0, 0 ]
wrongWordCount = [ 0.0, 0.0, 0.0, 0.0 ]
correctWordCount = [ 0.0, 0.0, 0.0, 0.0 ]
totalWordCount = [ 0.0, 0.0, 0.0, 0.0 ]

for message in spams.find():

	if "englishWords" not in message:
		continue

        if len(message['nonEnglishWords']) + len(message['englishWords']) > 0:
                messageCount[3] += 1
                if message['year'] == "2015":
                        messageCount[2] += 1

                elif message['year'] == "2014":
                        messageCount[1] += 1

                elif message['year'] == "2013":
                        messageCount[0] += 1


        totalWordCount[3] += len(message['englishWords'])
        totalWordCount[3] += len(message['nonEnglishWords'])
        correctWordCount[3] += len(message['englishWords'])
        wrongWordCount[3] += len(message['nonEnglishWords'])

        if message['year'] == "2015": 
                totalWordCount[2] += len(message['englishWords'])
                totalWordCount[2] += len(message['nonEnglishWords'])
                correctWordCount[2] += len(message['englishWords'])
                wrongWordCount[2] += len(message['nonEnglishWords'])

        elif message['year'] == "2014": 
                totalWordCount[1] += len(message['englishWords'])
                totalWordCount[1] += len(message['nonEnglishWords'])
                correctWordCount[1] += len(message['englishWords'])
                wrongWordCount[1] += len(message['nonEnglishWords'])

        elif message['year'] == "2013":
                totalWordCount[0] += len(message['englishWords'])
                totalWordCount[0] += len(message['nonEnglishWords'])
                correctWordCount[0] += len(message['englishWords'])
                wrongWordCount[0] += len(message['nonEnglishWords'])


print "Messages: " + str(messageCount[3])
print "Words: " + str(correctWordCount[3])
print "Errors: " + str(wrongWordCount[3])

print "Percentage 2013: " + str(wrongWordCount[0]/correctWordCount[0] *100)
print "Percentage2 2013: " + str(wrongWordCount[0]/totalWordCount[0] *100)

print "Percentage 2014: " + str(wrongWordCount[1]/correctWordCount[1] *100)
print "Percentage2 2014: " + str(wrongWordCount[1]/totalWordCount[1] *100)

print "Percentage 2015: " + str(wrongWordCount[2]/correctWordCount[2] *100)
print "Percentage2 2015: " + str(wrongWordCount[2]/totalWordCount[2] *100)

print "Percentage Total: " + str(wrongWordCount[3]/correctWordCount[3] *100)
print "Percentage2 Total: " + str(wrongWordCount[3]/totalWordCount[3] *100)
