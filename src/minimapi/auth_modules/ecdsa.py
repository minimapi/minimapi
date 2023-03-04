from functools import wraps
from flask import request, jsonify

from datetime import datetime
import ecdsa
from hashlib import sha512

MAX_TIMESTAMP_GAP = 3
HASH_FUNCTION = sha512
CURVE = ecdsa.NIST521p

class Auth:

	def __init__(self, database):
		self.database = database

	def check(self, function):
		@wraps(function)
		def wrapper(*args,**kargs):
			try:
				auth_data = request.headers.get('Authorization').split('.')
				if self.database.read('auth',id=auth_data[0]):
					public_key = self.database.read('auth',id=auth_data[0])[0]['public_key']
					signature_checker = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=CURVE, hashfunc=HASH_FUNCTION)
					timestamp = str(int(datetime.utcnow().timestamp()))
					payload = ((auth_data[2]+request.method+request.full_path.strip('?')).encode('utf-8')+request.data)
					if signature_checker.verify(bytes.fromhex(auth_data[1]), payload) and (abs(int(timestamp) - int(auth_data[2])) <= MAX_TIMESTAMP_GAP):
						return function(*args,**kargs)
			except:
				pass
			return '', 401
		return wrapper

	def login(self, request_data):
		public_key = request_data["public_key"]
		del request_data["public_key"]
		results = self.database.read('auth', **request_data)
		if len(results) == 1:
			self.database.update('auth', results[0]['id'], public_key=public_key)
			return jsonify({'id':results[0]['id']})
		return '', 401

	def logout(self, request):
		return '', 200