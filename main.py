# me_irl Image Downloader
# Author: Jay Bulsara

# uses leonardicus's imgur downloader: https://github.com/leonardicus/imgurdl

import logging
from os import listdir
import mimetypes

from archiveHelper import read, count
from downloadHelper import downloadHelper, download

def main():
	# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	numberOfMonths = 18
	numberOfScoreRanges = 5
	dateCol = 0
	imageCol = 1
	scoreCol = 2
	titleCol = 3
	userCol = 4
	postCol = 5

	# empty rogue_files.txt
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
	url = 'http://imgur.com/a/TuT7t'
	imagePath = downloadHelper(url)
	print(imagePath)


if __name__ == '__main__':
	main()