from functools import wraps

class Auth:

	def __init__(self, database):
		pass

	def check(self, function):
		@wraps(function)
		def wrapper(*args,**kargs):
			return function(*args,**kargs)
		return wrapper

	def login(self, request_data):
		return '', 404

	def logout(self, request):
		return '', 404