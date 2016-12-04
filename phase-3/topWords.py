from collections import Counter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from matplotlib import pyplot as plt
import numpy as np

client = MongoClient()    # Open client connection
db = client['spam-db']    # choose database
spams = db.spams          # this is our collection

wordCounter = Counter()

for message in spams.find():
	for word in message['nonEnglishWords']:

		wordCounter[word] += 1


word_label_list = list()
word_counter_list = list()
out_file = open("exportData",'w')
for word in wordCounter.most_common(100):
	out_file.write(word[0])
	out_file.write(",")
	out_file.write(str(word[1]))
	out_file.write(",")
	#word_label_list.append(word[0])
	#word_counter_list.append(word[1])

"""
spread = np.arange(100)
plt.bar(spread, word_counter_list, 0.35, color='r')
plt.set_xticks(spread)
plt.set_xticklabels(word_label_list)

plt.show()
"""
