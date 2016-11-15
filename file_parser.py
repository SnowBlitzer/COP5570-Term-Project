import os, sys, concurrent.futures

# Global data structures
emails = dict()
total_content = list()

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

def analyze_file(file_path):
	"""
	Handles a single file path.
	"""

	addFlag = False
	content = set()
	global total_content
	global emails

	with open(file_path,"r") as file_contents:
		#Iterate through file contents
		for line in file_contents:
			line_tokens = line.split()

			if len(line_tokens) > 1:
				#if the flag is set, clean up all the data.
				#Discard links and strip characters. Add it to the list
				if addFlag:
					content = content.union(clean_line(line_tokens))
				#Add the email to the hash table (counter)
				elif line_tokens[0] == "From:":
					if line_tokens[-1] in emails:
						emails[line_tokens[-1]] += 1
					else:
						emails[line_tokens[-1]] = 1
				#If the content is plain/text, set the addFlag
				elif line_tokens[1] == "text/plain" or line_tokens[1] == "text/plain;":
					addFlag = True
			elif len(line_tokens) == 1 and addFlag and not line_tokens[0].isalnum():
				addFlag = False
				break
		total_content.append(content)

def parse_files(path):
	"""
	Extracts content from all files within the given
	path.
	"""

	# Add missing / if needed
	if not path.endswith("/"):
		path += "/"

	def qualify(file_path):
		"""
		Approves files to be included in analysis.
		"""
		return os.path.isfile(file_path) and (file_path.endswith(".lorien"))

	#counter = 0

	#Look through all qualifying files in path
	files = (filename for filename in os.listdir(path) if qualify(path + filename))
	# for filename in files:
	# 	file_path = path + filename
	# 	analyze_file(file_path)
	# 	#counter += 1

	# code from stack_overflow
	executor = concurrent.futures.ThreadPoolExecutor(10)
	futures = [executor.submit(analyze_file, path + filename) for filename in files]
	concurrent.futures.wait(futures)

	final_content = [item for item in total_content if len(item) is not 0]


	print final_content
	#print counter
	#print emails

if __name__ == '__main__':
	if len(sys.argv) is not 2:
		print "usage: python %s pathname" % os.path.basename(__file__)
	else:
		path = sys.argv[1]
		parse_files(path)
