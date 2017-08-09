# This method returns a specific dump from the me_irl post archive
# based on the month and score range

# The month is determined by the index of that month's folder in
# archive/. They are listed in ascending order when returned by
# listDir.

from os import listdir
import logging
import codecs # to handle Unicode characters

def read(dateIndex, scoreRangeIndex):
	# archive configuration
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	# construct filepath
	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	# logging.info(filepath)
	
	# initialize post list - each row will contain a post with columns detailing post metadata
	posts = []
	
	# post titles may contain unicode characters, so the file must be opened with codecs.open()
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			# remove final carriage return and new line, split line by commas, then append as new row in posts.
			newPost = str.split(str.replace(line,'\r\n', ''), ',')
			posts.append(newPost)

	return posts

def count(dateIndex, scoreRangeIndex):
	# archive configuration
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	# construct filepath
	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	# logging.info(filepath)
	
	count = 0
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			count += 1

	return count

def countalbum(dateIndex, scoreRangeIndex):
	# archive configuration
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	# construct filepath
	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	# logging.info(filepath)
	
	count = 0
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			if '/a/' in line.split(',')[1]:
				count += 1

	return count

def countall(numberOfMonths, numberOfScoreRanges):
	postCount = []
	for i in range(numberOfMonths):
		row = [i]
		for j in range(numberOfScoreRanges):
			row.append(countalbum(i,j))
		postCount.append(row)
	return postCount

def write(posts):
	pass