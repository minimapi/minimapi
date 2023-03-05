class Type:

	@staticmethod
	def check(data):
		return isinstance(value, str)

	@staticmethod
	def request_task(data):
		import hashlib
		return hashlib.sha256(data.encode('utf-8')).hexdigest()