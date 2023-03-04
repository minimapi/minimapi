from flask import Flask, request, jsonify, send_from_directory, send_file
from .sanitizer import Sanitizer
import json
import __main__
from os.path import dirname

class Minimapi:

	def __init__(self, model_path, database_type, database_URI, auth_method='none'):
		self.path = dirname(__main__.__file__)
		self.lib_path = dirname(__file__)
		self.app = Flask(__name__)
		self.model_path = self.path+'/'+model_path
		self.model = self.load_model(self.model_path)
		database_connector = __import__('minimapi.database_connectors.'+database_type, fromlist=['Database'])
		self.database = database_connector.Database(database_URI)
		auth_module = __import__('minimapi.auth_modules.'+auth_method, fromlist=['Auth'])
		self.auth = auth_module.Auth(self.database)
		self.sanitizer = Sanitizer(self.model, self.database)
		self.add_routes()


	def load_model(self, path):
		# Load data self.model definition & add empty tags array if missing
		model = None
		with open(path, 'r') as model_file:
			model = json.load(model_file)
			for table in model:
				for property in model[table]:
					if 'tags' not in model[table][property]:
						model[table][property]['tags'] = []
		return model


	def serve_static(self, static_path):
		@self.app.route('/')
		def serve_index():
			return send_from_directory(self.path+'/'+static_path, 'index.html')
				
		@self.app.route('/<path:path>')
		def serve_static(path):
			return send_from_directory(self.path+'/'+static_path, path)


	def add_routes(self):

		@self.app.route('/api/auth', methods=['POST'])
		def login():
			request_data = self.sanitizer.sanitize_request('auth', request.json)
			if request_data:
				return self.auth.login(request_data)
			return 'Bad request', 400

		@self.app.route('/api/auth', methods=['DELETE'])
		@self.auth.check
		def logout():
			return self.auth.logout(request)
		
		@self.app.route('/api/model.json')
		@self.auth.check
		def send_model():
			return send_file(self.model_path)
		
		@self.app.route('/api/<table>', methods=['GET'])
		@self.auth.check
		def list(table):
			if table in self.model:
				if request.args:
					data = self.database.read(table, **request.args)
				else:
					data = self.database.read(table)
				return jsonify(self.sanitizer.sanitize_reponse(table, data, True))
			return 'Not found', 404
		
		@self.app.route('/api/<table>', methods=['POST'])
		@self.auth.check
		def create(table):
			request_data = self.sanitizer.sanitize_request(table, request.json)
			if request_data:
				data = self.sanitizer.sanitize_reponse(table, self.database.create(table,**request_data))
				return jsonify(data), 201
			return 'Bad request', 400
		
		@self.app.route('/api/<table>/<id>', methods=['GET'])
		@self.auth.check
		def read(table, id):
			if table in self.model:
				return jsonify(self.sanitizer.sanitize_reponse(table, self.database.read(table,id=id)))
			return 'Not found', 404
		
		@self.app.route('/api/<table>/<id>', methods=['PUT'])
		@self.auth.check
		def update(table, id):
			request_data = self.sanitizer.sanitize_request(table, request.json, True)
			if request_data:
				data = self.sanitizer.sanitize_reponse(table, self.database.update(table, id, **request.json))
				return jsonify(data), 201
			return 'Bad request', 400
		
		@self.app.route('/api/<table>/<id>', methods=['DELETE'])
		@self.auth.check
		def delete(table, id):
			if table in self.model:
				self.database.delete(table, id)
				return '', 204
			return 'Not found', 404