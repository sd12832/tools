import sys
import youtube_dl

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

	def YT_extract(self, link):

		with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
			ydl.download([link]) 

	    # TODO: output template the output
	    # TODO: 

		output_file_name = ''
		return output_file_name

	def SC_extract(self, link):

		output_file_name = ''
		return output_file_name
