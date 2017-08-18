# me_irl Image Downloader
# Author: Jay Bulsara

# uses leonardicus's imgur downloader: https://github.com/leonardicus/imgurdl

import logging
from os import listdir
import mimetypes
import traceback

from archiveHelper import ArchiveHelper
from downloadHelper import DownloadHelper

def main():
	# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	numberOfMonths = 18
	numberOfScoreRanges = 5

	archiveHelper = ArchiveHelper()

	for i in range(1): # months
		for j in range(1): # score buckets
			archiveHelper.setup(i,j)

			# read file line by line
			for line in archiveHelper.f:
				try:
					# extract post data
					archiveHelper.setPost(line)

					# send post to downloadHelper
					downloadHelper = DownloadHelper(archiveHelper.post)

					# run download helper
					downloadHelper.run()

					# transfer post to proper directory
					archiveHelper.transfer(downloadHelper.post, downloadHelper.outputFlag)

				except Exception as e:
					print('Error on post ' + archiveHelper.post['date'])
					traceback.print_exc()
					archiveHelper.transfer(downloadHelper.post, 'archive')

			archiveHelper.cleanup()


if __name__ == '__main__':
	main()
