# me_irl Image Downloader
# Author: Jay Bulsara

import psycopg2
import logging
from os import listdir

from archiveHelper import read
import mimetypes

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

	mimetypes.init()

	def getExtensionsForType(generalType):
		for ext in mimetypes.types_map:
			if mimetypes.types_map[ext].split('/')[0] == generalType:
				yield ext

	filetypes = tuple(getExtensionsForType('image'))
	domains = 'imgur', 'tumblr', 'gfycat', 'youtube', 'youtu.be', 'reddituploads', 'redditmedia', 'fbcdn'
	# skip youtube, fbcdn when downloading

	# empty file
	open('rogue_files.txt', 'w')
	
	for i in range(numberOfMonths):
		for j in range(1,numberOfScoreRanges):
			posts = read(i,j)
			for k in range(len(posts)):
				imageURL = posts[k][imageCol]

				# check if filetype or domain exists
				if not imageURL.endswith(filetypes) and not any(s in imageURL for s in domains):
					with open('rogue_files.txt','a') as f:
						f.write(imageURL + '\n')

if __name__ == '__main__':
	main()