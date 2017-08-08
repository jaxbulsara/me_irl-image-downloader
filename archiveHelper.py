from os import listdir
import logging
import codecs # to handle Unicode characters

def read(dateIndex, scoreRangeIndex):
	archiveFolder = 'archive'
	scoreRanges = ['0-50.txt', '51-500.txt', '501-1000.txt', '1001-5000.txt', '5001-inf.txt']
	dates = listdir(archiveFolder)

	filepath = archiveFolder + '/' + dates[dateIndex] + '/' + scoreRanges[scoreRangeIndex]
	print(filepath)
	posts = []
	with codecs.open(filepath, 'r', 'utf-8') as f:
		for line in f:
			posts.append(str.split(str.replace(line,'\r\n', ''), ','))

	return posts

	
