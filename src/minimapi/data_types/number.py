class Type:

	@staticmethod
	def check(data):
		return isinstance(data, int)

	@staticmethod
	def write(data):
		return input

	@staticmethod
	def read(data):
		return input