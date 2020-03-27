import sys, re, os
import unittest
import Hasher
from Downloader import *
from urllib.parse import urlparse
# TODO: Checks for particular libraries

SAMPLES = '/Users/sharanduggirala/Desktop/samples/'

# Test Variables
TEST = 0
YT_TEST_SONG = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'


def url_extract(link): 

	return urlparse(link).netloc

def main(link):

	# Check is sample folder exists
	if not os.path.isdir(SAMPLES):
		os.mkdir(SAMPLES)

	file_name = ''

	url = url_extract(link)
	DL = Downloader()

	if url == 'www.youtube.com':
		file_name = DL.YT_extract(link)
	elif url == 'www.soundcloud.com/':
		file_name = DL.soundcloud_extract(link)
	else:
		print('Link is not Youtube or Soundcloud. Please use either of the websites.')

	print(f'The output file name is {file_name}')


class MinerTest(unittest.TestCase): 
  
    def YT_test(self):         
        self.assertTrue(True) 

    def SC_Test(self):         
        self.assertTrue(True) 
  
if __name__== "__main__":
	if not TEST:
		main(sys.argv[1])
	else:
		unittest.main()


