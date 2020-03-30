import sys
import youtube_dl
# from sclib import SoundcloudAPI, Track, Playlist

class Downloader:

	def __init__(self, codec='wav', YDL_opts=None):

		self.codec = codec

		if self.codec == 'mp3' or codec == 'wav':

			if not YDL_opts:
					self.ydl_opts = {
				    'format': 'bestaudio/best',
				    'postprocessors': [{
				        'key': 'FFmpegExtractAudio',
				        'preferredcodec': 'wav',
				        'preferredquality': '192',
				    }],
				}

		else:
			print(f'{codec} is not a valid format')
			sys.exit(1)


	def get_latest_file(self):

		# HACK! Getting the latest changed file. Not so atomic 
		# but in practice  most probably not a problem

		import glob
		import os

		list_of_files = glob.glob(os.getcwd() + '/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		latest_file = latest_file.replace(os.getcwd() + '/', '')
		
		return latest_file


	def YT_extract(self, link):

		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			ydl.download([link])

		return self.get_latest_file()


	def SC_extract(self, link):

		# TODO: Try and look more into the SoundCloud API for universal downloads. 
		# Some websites manage it for some reason. Not sure why an API cannot. Has
		# to be a seperate project. 

		# api = SoundcloudAPI() 
		# track = api.resolve(link)
		# assert type(track) is Track

		# filename = f'./{track.artist} - {track.title}.mp3'

		# with open(filename, 'wb+') as fp:
		#     track.write_mp3_to(fp)

		return ''
