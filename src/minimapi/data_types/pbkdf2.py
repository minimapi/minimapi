class Type:

	@staticmethod
	def check(data):
		return isinstance(data, str)

	@staticmethod
	def request_task(data):
		import hashlib
		from os import urandom
		salt = urandom(32)
		min_rounds = 1000
		max_rounds = 2000
		bytes_count = (max_rounds - min_rounds + 1).bit_length() // 8 + 1
		rounds_bytes = urandom(bytes_count)
		rounds = int.from_bytes(rounds_bytes, byteorder="big") % (max_rounds - min_rounds + 1) + min_rounds
		h = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, rounds).hex()
		result = '{}.{}.{}'.format(rounds, salt.hex(), h)
		return result

	@staticmethod
	def comparison_task(input_data, stored_data):
		try:
			import hashlib
			stored_data_array = stored_data.split('.')
			h = hashlib.pbkdf2_hmac('sha256', input_data.encode(), bytearray.fromhex(stored_data_array[1]), int(stored_data_array[0])).hex()
			return (h == stored_data_array[2])
		except:
			pass
		return False