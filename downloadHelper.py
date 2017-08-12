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

		# to check whether the download is to proceed or has succeeded
		self.downloadFlag = True

		# initialize download arguments dict
		self.args = {}

		# initialize post info list
		self.post = {}

		# output flag: rogue, removed, downloaded, skipped, archive
		# this is the folder the post will be moved to
		self.outputFlag = ''


	def analyze(self):
		# analyzes an image url and checks if it contains a known filetype or domain. If not, the url is marked as rogue. If either exist, the download is viable and and argument list is built

		# reset args
		self.args = {}

		url = self.post['imageurl']
		self.args['url'] = url

		# no file extension and no known domain - rogue
		if not url.split('?')[0].endswith(self.filetypes)and not any(s in url for s in self.domains):
			self.downloadFlag = False
			self.outputFlag = 'rogue'

		# either a proper domain or a file extension exist
		else:
			for s in self.domains:
				if s in url:
					self.args['domain'] = s
					break

			if url.split('?')[0].endswith(self.filetypes):
				self.args['fileExt'] = '.' + url.split('?')[0].split('.')[-1]
				if self.args['fileExt'] == '.gifv':
					self.args['fileExt'] = '.gif'
					url = url.replace('gifv', 'gif')
					self.post['imageurl'] = url
					self.args['url'] = url


	def download(self, url, domain='', fileExt=''):
		# parse url to determine how it should be handled
		# if the image downloads successfully, imagepath defines where it was saved and outputFlag is set to 'downloaded'
		# if the image fail to download, imagepath is blank and outputFlag is set to 'removed'
		# if the url is youtube, imagepath is blank and outputFlag is set to 'video'

		if domain == 'imgur':
			if fileExt != '':
				# cut off file extension as it is not supported by imgurdl
				url = url.split(fileExt)[0]
			self.downloadImgur(url)

		elif domain == 'youtube' or domain == 'youtu.be':
			self.post['imagepath'] = ''
			self.outputflag = 'video'

		elif domain == 'fbcdn':
			self.downloadFacebook(url)

		elif fileExt != '':
			self.downloadGeneral(url)

		elif domain == 'reddituploads':
			self.downloadReddituploads(url)

		elif domain == 'gfycat':
			self.downloadGfycat(url)

		else:
			raise Exception


	def downloadGeneral(self, url):
		# urls with an image and a known extension
		# should be pretty straightforward
		self.post['imagepath'] = ''
		self.outputFlag = 'archive'

	def downloadImgur(self, url):
		# use ImgurDL
		self.post['imagepath'] = ''
		self.outputFlag = 'archive'


	def downloadFacebook(self, url):
		# need to get me_irl post url for the picture
		self.post['imagepath'] = ''
		self.outputFlag = 'archive'


	def downloadReddituploads(self, url):
		# need to find out image type when http request is made
		self.post['imagepath'] = ''
		self.outputFlag = 'archive'


	def downloadGfycat(self, url):
		# gotta parse html page for the image
		self.post['imagepath'] = ''
		self.outputFlag = 'archive'


	def setPost(self, post):
		self.post = post


	def getExtensionsForType(self, generalType):
		for ext in mimetypes.types_map:
			if mimetypes.types_map[ext].split('/')[0] == generalType:
				yield ext
			yield '.gifv'


	def run(self):
		# analyze the post
		self.analyze()

		# if url is viable, download image
		if self.downloadFlag:
			self.download(**self.args)
