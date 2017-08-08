from imgurdl import ImgurDL
import mimetypes
import logging

def downloadHelper(url):
	mimetypes.init()

	filetypes = tuple(getExtensionsForType('image'))
	domains = 'imgur', 'tumblr', 'gfycat', 'youtube', 'youtu.be', 'reddituploads', 'redditmedia', 'fbcdn'

	# no file extension and no domain - rogue
	if not url.split('?')[0].endswith(filetypes) and not any(s in url for s in domains):
		with open('rogue_files.txt','a') as f:
			# logging.info('rogue file: ' + url)
			f.write(url + '\n')

	# either a proper domain or a file extension exist
	else:
		args = {'url': url}

		for s in domains:
			if s in url:
				args['domain'] = s
				break
		# logging.info('domain = ' + domain)

		if url.split('?')[0].endswith(filetypes):
			args['fileExt'] = '.' + url.split('?')[0].split('.')[-1]
			# logging.info('has file extension ' + fileExt)

		imagePath = download(**args)


	return imagePath

def getExtensionsForType(generalType):
	for ext in mimetypes.types_map:
		if mimetypes.types_map[ext].split('/')[0] == generalType:
			yield ext

def download(url, domain='', fileExt=''):
	logging.debug('{0}, {1}'.format(domain, fileExt))
