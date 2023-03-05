class Type:

	@staticmethod
	def check(data):
		return isinstance(data, str)

	@staticmethod
	def comparison_task(input_data, stored_data):
		import pyotp
		import time
		return (input_data == pyotp.TOTP(stored_data).now())