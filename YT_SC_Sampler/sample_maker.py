import sys, re, os, unittest
from Hasher import Hasher
from Detect import Detect
from Downloader import Downloader
from urllib.parse import urlparse
import music21

# TODO: Checks for particular libraries

SAMPLES = os.path.expanduser("~") + '/Desktop/samples/'

# Test Variables
TEST = 0
YT_TEST_SONG = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


def detect_key(wav_location):
	D = Detect()
	bpm = D.detect(wav_location)
	sys.exit(1)
	score = music21.converter.parse(os.getcwd() + '/' + file_name)
	key1 = score.analyze('Krumhansl')
	key2 = score.analyze('AardenEssen')
	if key1 != key2: 
		print(key1, key2)
	else:
		print(key1)
  

def url_extract(link): 

	return urlparse(link).netloc


def extract(link):

	# Check is sample folder exists
	if not os.path.isdir(SAMPLES):
		os.mkdir(SAMPLES)

	file_name = ''

	url = url_extract(link)
	DL = Downloader()

	if url == 'www.youtube.com':
		file_name = DL.YT_extract(link)

		os.rename(os.getcwd() + '/' + file_name, 
			SAMPLES + file_name.replace(' (Video)-' +
										 link.split('=')[-1], ''))

		detect_key(SAMPLES + file_name.replace(' (Video)-' +
										 link.split('=')[-1], ''))

	elif url == 'soundcloud.com':
		file_name = DL.SC_extract(link)
		print('Currently not supporting Soundcloud due to API Issues.')
		sys.exit(1)

	else:
		print('Link is not Youtube or Soundcloud.')
		print('Please use either of the websites.')
		sys.exit(1)

	return file_name


def main(link):

	file_name = extract(link)
	print(f'The output file name is {file_name}')


class Test(unittest.TestCase): 

	# def __init__(self, *args, **kwargs):
	# 	super(TestingClass, self).__init__(*args, **kwargs)
	# 	self.H = Hasher()


	def test_YT(self): 
		self.H = Hasher()
		self.assertTrue(True) 

		if os.path.exists(os.getcwd() + '/' + 'test_hash.txt'):
			file_name = extract(YT_TEST_SONG)
			comp = self.H.compare_file_txt(SAMPLES + file_name.replace(' (Video)-' + 
							YT_TEST_SONG.split('=')[-1], ''), 
							os.getcwd() + '/' + 'test_hash.txt')
			self.assertTrue(comp)

		else:

			H.YT_create_hash(YT_TEST_SONG)
			print('Test Hash was not created till now. Test Again')


	def test_SC(self):    

		self.assertTrue(True) 
  
if __name__== "__main__":

	if TEST:
		unittest.main()
	else:
		main(sys.argv[1])