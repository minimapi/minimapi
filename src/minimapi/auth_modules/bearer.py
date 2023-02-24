from functools import wraps
from flask import request

class Auth:

	def __init__(self, database):
		self.database = database

	def check(self, function):
		@wraps(function)
		def wrapper(*args,**kargs):
			try:
				token = request.headers.get('Authorization').split(' ')[1]
				if self.database.read('auth',token=token):
					return function(*args,**kargs)
			except:
				pass
			return '', 401
		return wrapper

	def login(self, request_data):
		return '', 404

	def logout(self, request):
		return '', 404