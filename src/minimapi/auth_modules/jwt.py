from functools import wraps
from flask import request, jsonify

import jwt
from os import urandom
from datetime import datetime, timedelta, timezone

JWT_ALGO = "HS256"
JWT_SECRET_SIZE = 64
JWT_EXPIRATION_IN_MIN = 60

class Auth:

	def __init__(self, database):
		self.database = database
		self.secret = urandom(JWT_SECRET_SIZE)

	def check(self, function):
		@wraps(function)
		def wrapper(*args,**kargs):
			try:
				auth_data = jwt.decode(request.headers.get('Authorization'), self.secret, algorithms=[JWT_ALGO])
				if self.database.read('auth',id=auth_data['ID']):
					return function(*args,**kargs)
			except:
				pass
			return '', 401
		return wrapper

	def login(self, request_data):
		results = self.database.read('auth', **request_data)
		if len(results) == 1:
			return jsonify({'token': jwt.encode({"ID": results[0]['id'], "exp": datetime.now(tz=timezone.utc)+timedelta(minutes=JWT_EXPIRATION_IN_MIN)}, self.secret, algorithm=JWT_ALGO)})
		return '', 401

	def logout(self, request):
		return '', 200