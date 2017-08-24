from imgurdl import ImgurDL
import mimetypes
import os
import urllib3
import certifi
import shutil
import requests
from bs4 import BeautifulSoup as bs
from time import sleep

class DownloadHelper():
	def __init__(self, post):
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
		self.post = post

		# output flag: rogue, removed, downloaded, archive, youtube
		# this is the folder the post will be moved to
		self.outputFlag = ''

		# Establish a HTTP connection pool manager
		self.http = urllib3.PoolManager(
			cert_reqs='CERT_REQUIRED',
			ca_certs=certifi.where())

	def analyze(self):
		# analyzes an image url and checks if it contains a known filetype or domain. If not, the url is marked as rogue. If either exist, the download is viable and and argument list is built

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
				if self.args['fileExt'] == '.gif':
					self.args['fileExt'] = '.gifv'
					url = url.replace('gif', 'gifv')
					self.args['url'] = url

	def download(self, url, domain='', fileExt=''):
		# parse url to determine how it should be handled
		link = ''

		if domain == 'imgur' and fileExt == '':
			link = self.parseImgur(url)

		elif domain == 'youtube' or domain == 'youtu.be':
			link = ''
			self.outputflag = 'youtube'

		elif domain == 'fbcdn':
			link = self.parseReddit()

		elif fileExt != '':
			link = url

		elif domain == 'reddituploads':
			link = self.parseReddit()

		elif domain == 'gfycat':
			link = self.parseGfycat(url)

		# download image(s)
		if not self.outputFlag:
			try:
				self.saveImage(link)
			except urllib3.exceptions.MaxRetryError as e:
				print('Connection failed on: ' + self.post['date'])
				print('Trying to download from reddit.')
				link = self.parseReddit()
				self.saveImage(link)


	def parseImgur(self, url):
		albumFlag = False

		# check if link is an album
		if '/a/' in url:
			albumFlag = True

		# get imgur page

		# All of the image links are inside div tags in the body
		html = self.http.urlopen('GET', url, preload_content = False)
		# Make sure a successful HTTP request was made.
		if html.status != 200:
			print("HTTP {0}, skipping {1}".format(html.status, self.post['date']))
			self.outputFlag = 'removed'
			return ''

		# create BeautifulSoup object for html parsing
		soup = bs(html.data, 'html.parser')

		# set up list for links
		links = []

		# find all post image and video (gifv) links
		data = soup.findAll('div', attrs={'class':'post-image'})
		for div in data:
			for a in div:
				if a.name == 'img':
					links.append('https:' + a['src'])
				# if image is in a zoom container
				if a.name == 'a':
					links.append('https:' + a['href'])
				# if the image is a gifv, imgur converts it into a video
				# download the mp4 version
				if a.name == 'div':
					for b in a:
						if b.name == 'meta':
							if 'mp4' in b['content']:
								links.append(b['content'])

		if len(links) == 1:
			return links[0]
		else:
			return links

	def parseReddit(self):
		# go to reddit post to find image url
		url = 'https://reddit.com' + self.post['posturl']

		# All of the image links are inside div tags in the body
		html = self.http.urlopen('GET', url, preload_content = False)

		# Make sure a successful HTTP request was made.
		if html.status != 200:
			print("HTTP {0}, skipping {1}".format(html.status, self.post['date']))
			self.outputFlag = 'removed'
			return ''

		# create BeautifulSoup object for html parsing
		soup = bs(html.data, 'html.parser')

		data = soup.find('img', attrs={'class':'preview'})

		return data['src']

	def parseGfycat(self, url):
		# parse page header for video url

		# All of the image links are inside div tags in the body
		html = self.http.urlopen('GET', url, preload_content = False)

		# Make sure a successful HTTP request was made.
		if html.status != 200:
			print("HTTP {0}, skipping {1}".format(html.status, self.post['date']))
			self.outputFlag = 'removed'
			return ''

		# create BeautifulSoup object for html parsing
		soup = bs(html.data, 'html.parser')

		# find meta tag with video in it
		data = soup.find('meta', attrs={'property':'og:video'})

		return data["content"]

	def saveImage(self, link):
		out_path = os.path.join('images', self.post['date'].replace(':', '-'))
		if link and type(link) == str:
			fileExt = '.' + link.split('?')[0].split('.')[-1]
			out_path = out_path + fileExt
			r = self.http.request('GET', link, preload_content=False)
			isRemoved = False
			try:
				if r.getheaders()['ETag'] == '"d835884373f4d6c8f24742ceabe74946"':
					isRemoved = True
					outputFlag = 'removed'
			except KeyError:
				pass
			finally:
				if not isRemoved:
					try:
						with open(out_path, 'wb') as out_file:
							shutil.copyfileobj(r, out_file)
					except FileNotFoundError:
						os.makedirs('images')
						with open(out_path, 'wb') as out_file:
							shutil.copyfileobj(r, out_file)
					self.outputFlag = 'downloaded'
					print('Downloaded: {} as {}'.format(link, out_path))
			sleep(0.5)

		elif link and type(link) == list:
			i = 0
			for lin in link:
				fileExt = '.' + lin.split('?')[0].split('.')[-1]
				out_path_num = out_path + '_{0:02d}'.format(i) + fileExt
				with self.http.request('GET', lin, preload_content=False) as r, open(out_path_num, 'wb') as out_file:
					shutil.copyfileobj(r, out_file)
				i += 1
				sleep(0.5)
			self.outputFlag = 'downloaded'

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
