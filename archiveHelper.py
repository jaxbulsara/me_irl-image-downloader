# The month is determined by the index of that month's folder in
# archive/. They are listed in ascending order when returned by
# listDir.

import os
import logging
import codecs # to handle Unicode characters

class ArchiveHelper():
	def __init__(self):
		# file indentifiers
		self.dateIndex = 0
		self.scoreRangeIndex = 0

		# folder names
		self.archive = 'archive'
		self.rogue = 'rogue'
		self.removed = 'removed'
		self.downloaded = 'downloaded'
		self.video = 'video'

		self.scoreRanges = ['5001-inf.txt', '1001-5000.txt', '501-1000.txt', '51-500.txt','0-50.txt']
		self.dates = os.listdir(self.archive)

		# filenames
		self.filename = ''
		self.tempFilename = ''

		# file for reading
		self.f = ''

		# read/write counters
		self.readCount = 0
		self.writeCount = 0
		self.writeFlag = False

		# initialze post info container
		self.post = {}


	def setup(self, dateIndex, scoreRangeIndex):
		# sets up the data filename based on indentifiers and creates a temp file and opens it to read

		# construct filename based on date and score range
		self.filename = os.path.join(self.dates[dateIndex], self.scoreRanges[scoreRangeIndex])

		# construct temp filename in archive
		self.tempFilename = self.filenameIn(self.archive) + '.tmp'

		# create temp file for reading
		os.rename(self.filenameIn(self.archive), self.tempFilename)

		# open temp file for reading
		self.f = codecs.open(self.tempFilename, 'r', 'utf-8')


	def filenameIn(self, folder):
		# returns a path to the data file inside the specified folder
		return os.path.join(folder, self.filename)


	def setPost(self, line, postfields = ['date', 'imageurl', 'score', 'title', 'user', 'posturl']):
		i = 0

		for field in str.split(str.replace(line,'\r\n', ''), ','):
			self.post[postfields[i]] = field
			i += 1


	def transfer(self, folder):
		print('Entered archiveHelper.transfer()')

	def cleanup(self):
		self.f.close()

		# if no writes occur, rename temp file back to original
		if self.writeFlag == False:
			os.rename(self.tempFilename, self.filenameIn(self.archive))

		# if writes occur and no lines are lost, delete temp file
		elif self.readCount == self.writeCount:
			os.remove(self.tempFilename)

		else:
			print('Error: some lines were lost when processing ' + self.filename)
