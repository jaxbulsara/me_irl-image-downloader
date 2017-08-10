from imgurdl import ImgurDL
import mimetypes
import os
import urllib3

class DownloadHelper():
	def __init__(self):
		# setup mimetypes
		mimetypes.init()
		self.filetypes = tuple(self.getExtensionsForType('image'))
		
		# domains that require special handling
		self.domains = ('imgur', 'gfycat', 'youtube', 'youtu.be', 'reddituploads', 'fbcdn')

		# to check whether the helper should try and download an image
		self.downloadFlag = False

		# output flag: rogue, removed, downloaded, skipped
		self.outputFlag = ''

		# initialize download arguments dict
		self.args = {}

		# initialize post info list
		self.post = {}


	def analyze(self):
		# analyzes an image url and checks if it contains a known filetype or domain. If not, the url is marked as rogue. If either exist, the download is viable and and argument list is built

		url = self.post['imageurl']

		# no file extension and no known domain - rogue
		if not url.split('?')[0].endswith(self.filetypes) and not any(s in url for s in self.domains):
			self.outputFlag = 'rogue'

		# either a proper domain or a file extension exist
		else:
			self.downloadFlag = True
			self.args['url'] = url

			for s in self.domains:
				if s in url:
					self.args['domain'] = s
					break

			if url.split('?')[0].endswith(self.filetypes):
				self.args['fileExt'] = '.' + url.split('?')[0].split('.')[-1]


	def test(self):
		print('Entered downloadHelper.test()')
		pass


	def setPost(self, post):
		self.post = post


	def getExtensionsForType(self, generalType):
		for ext in mimetypes.types_map:
			if mimetypes.types_map[ext].split('/')[0] == generalType:
				yield ext


	def run(self):
		# analyze the post
		self.analyze()

		# if url is viable, test if the image exists online
		if self.downloadFlag:
			self.test()
