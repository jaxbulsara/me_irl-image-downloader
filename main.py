# me_irl Image Downloader
# Author: Jay Bulsara

# This script will read through scraped data from reddit.com/r/me_irl
# and download images posted to the site and maintain post metadata

class Reader():
	# reads through the data dump and pulls specific files to read
	archiveFolder = 'archive'
	dateFormat = '%d-%d'
	scoreRanges [] = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']