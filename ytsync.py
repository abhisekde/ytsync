#!/usr/bin/env python
# @program: automatic playlist syncup with music library
# @author: abhisek.de@live.com
import sys, requests, bs4, os, re
from ytmp3 import download_yt
from json import loads

def load_yt_pl(pl_link, dl_dir):
	v_list = {}
	err_list = []
	try:
		#Fetch Playlist items
		res = requests.get(pl_link)
		soup = bs4.BeautifulSoup(res.text, "lxml")
		plist = soup.select('.pl-video')
		if plist == []:
			print 'Playlist failed to load or Playlist empty.'
			exit(1)

		#Create (Song title, Link) pairs
		for v in plist:
			v_id = v.get('data-video-id')
			v_url = 'https://www.youtube.com/watch?v=' + v_id
			# print v_url
			url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video=' +  v_url
			response = requests.get(url)
			# print 'Response', response.text
			# Load JSON data into a Python variable.
			if response.text.startswith('<meta http-equiv="refresh" content="0;'):
				err_list.append(v_url)
			else:
				mp3 = loads(response.text)
				# print response.text
				v_title = mp3['title']
				# print mp3
				v_fname = re.sub("[^\w-]", "_", v_title) + '.mp3'
				v_list[v_fname] = v_url 
		
		#Select the new files that are to be downloaded. Discard exisitng files
		mp3_files = [f for f in os.listdir(dl_dir) if os.path.isfile(os.path.join(dl_dir, f)) and f.endswith('.mp3')]
		pl_files = v_list.keys()
		
		# Delete files from disc which are not in PL, and those which are present in FS and also in PL should be removed from list to be downloaded
		for fname in mp3_files:
			if fname not in pl_files:
				os.remove(os.path.join(dl_dir,fname))
			else:
				pl_files.remove(fname)
	
		#Download the files
		for fname in pl_files:
			download_yt(v_list[fname], dl_dir)

		# Print error list if, any
		if len(err_list) > 0:
			print 'Failed to fetch video information for the following links:'
			for i in err_list:
				print i

	except Exception as ex:
		print 'Error: ', str(ex)
		exit(1)

def main():
	if len(sys.argv) != 3:
		print 'Usage: ', sys.argv[0], 'https://www.youtube.com/playlist?list=UrlOfPlayListToDownload /path/to/music/library'
		exit(1)
	folder = os.path.abspath(sys.argv[2])
	if os.path.exists(folder) and os.path.isdir(folder):
		load_yt_pl(sys.argv[1], folder)
	else:
		print 'Error: Target folder does not exist'
		exit(1)

if __name__ == '__main__':
	main()
