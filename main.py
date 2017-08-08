# me_irl Image Downloader
# Author: Jay Bulsara

# uses leonardicus's imgur downloader: https://github.com/leonardicus/imgurdl

import logging
from os import listdir
import mimetypes

from archiveHelper import read, count
from downloadHelper import downloadHelper

def main():
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
	numberOfMonths = 18
	numberOfScoreRanges = 5
	dateCol = 0
	imageCol = 1
	scoreCol = 2
	titleCol = 3
	userCol = 4
	postCol = 5

	# empty file
	open('rogue_files.txt', 'w')
	
	# for i in range(numberOfMonths):
	# 	for j in range(1,numberOfScoreRanges):
	# 		posts = read(i,j)
	# 		for k in range(len(posts)):
	# 			imageURL = posts[k][imageCol]
	# 			download(imageURL)

	# posts = read(0,0)
	# for k in range(100):
	# 	imageURL = posts[k][imageCol]
	# 	downloadHelper(imageURL)

	with open('postCounts.csv', 'w') as f:
		for i in range(numberOfMonths):
			f.write(str(i) + ',')
			for j in range(numberOfScoreRanges):
				postCount = count(i, j)
				f.write(str(postCount))
				if j < numberOfScoreRanges - 1:
					f.write(',')
				else:
					f.write('\n')
				

if __name__ == '__main__':
	main()