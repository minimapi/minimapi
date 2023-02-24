class Type:

	@staticmethod
	def check(data):
		return isinstance(data, str)

	@staticmethod
	def write(data):
		return input

	@staticmethod
	def read(data):
		return input