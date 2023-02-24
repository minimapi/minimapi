import hashlib

class Type:

	@staticmethod
	def check(data):
		return isinstance(value, str)

	@staticmethod
	def write(data):
		return hashlib.sha256(data.encode('utf-8')).hexdigest()

	@staticmethod
	def read(data):
		return data