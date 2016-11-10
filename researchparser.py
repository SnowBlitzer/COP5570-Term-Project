import os

charactersToBeStripped = ".,;<>:[]\"|"

#Function strips all unneeded characters away and 
#hands back a unique set of all words greater than
#2 Characters
def cleaner(lineHandedIn):
	uniqueSet = set()
	for x in lineHandedIn:
		charStrippedText = x.strip(charactersToBeStripped)
		if len(charStrippedText) > 2 and charStrippedText.isalpha():
			uniqueSet.add(charStrippedText)
	return uniqueSet


emails = dict()
content = set()
totalContent = list()
addFlag = 0
#Look through all files in current directory
for fileName in os.listdir('.'):
	if os.path.isfile(fileName):
		#Open the file
		with open(fileName,"r") as fileContents:
			#Iterate through file contents
			for line in fileContents:
				#print line
				tempLine = line.split()
				if len(tempLine) > 1:
					#if the flag is set, clean up all the data. 
					#Discard links and strip characters. Add it to the list
					if addFlag == 1:
						content = content.union(cleaner(tempLine))
					#Add the email to the hash table
					elif tempLine[0] == "From:":
						if tempLine[-1] in emails:
							emails[tempLine[-1]] += 1
						else:
							emails[tempLine[-1]] = 1
					#If the content is plain/text, set the addFlag
					elif tempLine[1] == "text/plain" or tempLine[1] == "text/plain;":
						addFlag = 1
				elif len(tempLine) == 1 and addFlag == 1 and not tempLine[0].isalnum():
					break
			totalContent.append(content)
	#print content
