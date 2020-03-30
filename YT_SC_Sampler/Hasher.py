import hashlib

class Hasher:

	def __init__(self, hash_algo='md5'): 
		# TODO: support for more hash algos
		self.hash_algo = hash_algo 


	def hash_file(self, filename):

		return hashlib.md5(open(filename, 'rb').read()).hexdigest()


	def compare_file_txt(self, filename, hash_txt_file):
		# Useful for when there is an MD5 txt in the folder

		hash1 = self.hash_file(filename)

		if hash1 == open(hash_txt_file).readline():
			return True

		return False


	def YT_create_hash(self, link, output_loc='test_hash.txt'):

		DL = Downloader()
		file_name = DL.YT_extract(link)
		hash_txt = self.hash_file(os.getcwd() + '/' + file_name)
		o_file = open(output_loc, 'w')
		o_file.write(hash_txt)
		o_file.close()

