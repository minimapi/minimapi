from os import listdir
from os.path import dirname

class Sanitizer:

	def __init__(self, model, database=None):
		self.model = model
		self.database = database
		self.types = self.load_data_types()

	def load_data_types(self):
		types = dict()
		for filename in listdir(dirname(__file__)+'/data_types'):
			if filename.endswith('.py'):
				type_name = filename.split('.')[0]
				types[type_name] = __import__('minimapi.data_types.'+type_name, fromlist=['Type']).Type
		return types

	def check_type(self, type, key, value):
		if type == 'foreign':
			return ((not self.database) or (key in self.model and self.database.read(key, id=value)))
		elif type in self.types:
			return self.types[type].check(value)
		return False

	def sanitize_request(self, table, data, allow_missing=False):
		if table not in self.model:
			return False

		for property in data:
			if property in self.model[table]:
				if 'tags' in self.model[table][property] and 'encrypted' in self.model[table][property]['tags']:
					type_to_check = 'text'
				else:
					type_to_check = self.model[table][property]['type']
				
				if not self.check_type(type_to_check, property, data[property]):
					return False
			else:
				return False
		
		if not allow_missing:
			for property in self.model[table]:
				if property not in data:
					if 'tags' in self.model[table][property] and 'required' in self.model[table][property]['tags']:
						return False
					else:
						data[property] = None

		return data

	def sanitize_reponse(self, table, data, listing=False):
		data_to_return = []

		if table not in self.model:
			return None

		for result in data:
			row = {}
			for property in result:
				if property == 'id':
					row[property] = result[property] 
				elif property in self.model[table]:
					if 'tags' in self.model[table][property]:
						if 'unlistable' in self.model[table][property]['tags'] and listing:
							row[property] = '-'
							continue
					row[property] = result[property]
					 
			data_to_return.append(row)
		return data_to_return