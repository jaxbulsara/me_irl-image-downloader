# me_irl Image Downloader
# Author: Jay Bulsara

# uses leonardicus's imgur downloader: https://github.com/leonardicus/imgurdl

import logging
from os import listdir
import mimetypes

from archiveHelper import ArchiveHelper
from downloadHelper import DownloadHelper

def main():
	# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	numberOfMonths = 18
	numberOfScoreRanges = 5

	archiveHelper = ArchiveHelper()
	downloadHelper = DownloadHelper()

	for i in range(1): # months
		for j in range(1): # score buckets
			archiveHelper.setup(i,j)

			try:
				f = open('testing/sortTest.txt', 'w')

				# read file line by line
				for line in archiveHelper.f:
					# extract post data
					archiveHelper.setPost(line)

					# send post to downloadHelper
					downloadHelper.setPost(archiveHelper.post)

					# run download helper
					downloadHelper.run()

					# debugging - only read first post
					# break

			finally:
				f.close()
				archiveHelper.cleanup()


if __name__ == '__main__':
	main()
