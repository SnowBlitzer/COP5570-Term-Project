from collections import Counter
from matplotlib import pyplot as plt
import numpy as np
import sys

word_counter_list = list()
word_label_list = list()
with open(sys.argv[1],"r") as file:
	for line in file:
		word_counter_list =  line.split(",")[1::2]
		word_label_list = line.split(",")[::2]

spread = np.arange(len(word_counter_list))
plt.bar(spread, word_counter_list, 0.35, color='r',align='center')
ax = plt.gca()
ax.set_xticks(spread)
ax.set_xticklabels(word_label_list, rotation=90)

plt.show()
