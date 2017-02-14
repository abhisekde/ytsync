#!/usr/bin/env python
# @program: ytmp3.py - YouTube to MP3 Downloader
# @author: abhisek.de@live.com

import requests, io, os
from json import loads
from sys import exit, argv
from re import sub 
def download_yt(yt_url, folder):
	# Download the JSON data from www.youtubeinmp3.com API
	try:
		url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video=' +  yt_url
		response = requests.get(url)
		#response.raise_for_status()
		
		# Load JSON data into a Python variable.
		mp3 = loads(response.text)
		title = mp3['title']
		link = mp3['link']
	except Exception as ex:
		print 'Error: No video found at ', yt_url
		exit(1)
	
	# Load JSON data into variables.
	mp3 = loads(response.text)
	title = mp3['title']
	link = mp3['link']
	try:
		# Normalize the file name
		folder = os.path.abspath(folder)
		if os.path.exists(folder) and os.path.isdir(folder):
			file_name = os.path.join(folder, sub("[^\w-]", "_", title) + '.mp3')
		else:
			raise IOError('Path not found')
		# Download and save MP3 file
		res = requests.get(link)
		#res.raise_for_status()

		mp3_file = io.open(file_name, 'wb')
		for chunk in res.iter_content(100000):
			mp3_file.write(chunk)
		mp3_file.close()
	except Exception as e:
		print 'Error: In saving file.', str(e)
		exit(1)

def main():
	# Validate call
	if len(argv) < 3:
	    print 'Usage: ', argv[0], ' http://youtube.com/watch?v=VideoURL /path/to/music/library' 
	    exit()
	
	yt_url = argv[1]
	folder = argv[2]

	# Download Music
	download_yt(yt_url, folder)

if __name__ == '__main__':
	main()
