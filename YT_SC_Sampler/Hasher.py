# Hashes a file/uses Downloader.py to download and 

class Hasher:

	import hashlib 

	def __init__(self, hash_algo='md5'): 

		# TODO: support for more sums
		self.hash_algo = hash_algo 


	def hash_file(self, filename):

		return hashlib.md5(open(filename, 'rb').read()).hexdigest()


	def download_hash_file(self, file):

		return

	def compare_txt_hash(self, filename, hash_txt):

		hash1 = hashlib.md5(open(filename1, 'rb').read()).hexdigest()

		if hash1 == hash_txt:
			return True

		return False


	def compare_file_hash(self, filename, filename2):

		hash1 = hashlib.md5(open(filename1, 'rb').read()).hexdigest()
		hash2 = hashlib.md5(open(filename2, 'rb').read()).hexdigest()

		if hash1 == hash2:
			return True

		return False


	def download_txt_hash(self, link, hash_txt):

		return
