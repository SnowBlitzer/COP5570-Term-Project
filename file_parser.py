import os, sys


def clean_line(lineHandedIn):
	"""
	Function strips all unneeded characters away and
	hands back a unique set of all words greater than
	2 Characters
	"""
	charactersToBeStripped = ".,;<>:[]\"|"
	uniqueSet = set()
	for x in lineHandedIn:
		charStrippedText = x.strip(charactersToBeStripped)
		if len(charStrippedText) > 2 and charStrippedText.isalpha():
			uniqueSet.add(charStrippedText)
	return uniqueSet


def parse_files(path):
	"""
	Extracts content from all files within the given
	path.
	"""
	# Add missing / if needed
	if not path.endswith("/"):
		path += "/"

	emails = dict()
	content = set()
	totalContent = list()
	addFlag = False

	#Look through all files in current directory
	for filename in os.listdir(path):
		file_path = path + filename
		if os.path.isfile(file_path):
			#Open the file
			with open(file_path,"r") as file_contents:
				#Iterate through file contents
				for line in file_contents:
					#print line
					line_tokens = line.split()
					if len(line_tokens) > 1:
						#if the flag is set, clean up all the data.
						#Discard links and strip characters. Add it to the list
						if addFlag:
							content = content.union(clean_line(line_tokens))
						#Add the email to the hash table
						elif line_tokens[0] == "From:":
							if line_tokens[-1] in emails:
								emails[line_tokens[-1]] += 1
							else:
								emails[line_tokens[-1]] = 1
						#If the content is plain/text, set the addFlag
						elif line_tokens[1] == "text/plain" or line_tokens[1] == "text/plain;":
							addFlag = True
					elif len(line_tokens) == 1 and addFlag and not line_tokens[0].isalnum():
						break
				totalContent.append(content)
	print totalContent

if __name__ == '__main__':
	if len(sys.argv) is not 2:
		print "usage: python %s pathname" % os.path.basename(__file__)
	else:
		path = sys.argv[1]
		parse_files(path)
