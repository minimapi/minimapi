from pysondb import db

class Database:

	def __init__(self, URI):
		self.db_path = URI

	def create(self, table, **data):
		session = db.getDb(self.db_path+table+'.json')
		new_id = session.add(data)
		return self.read(table, id=new_id)

	def read(self, table, **filters):
		session = db.getDb(self.db_path+table+'.json')
		if 'id' in filters:
			filters['id'] = int(filters['id'])
		results = session.getBy(filters)
		for result in results:
			result['id'] = str(result['id'])
		return results

	def update(self, table, id, **data):
		session = db.getDb(self.db_path+table+'.json')
		data = session.updateById(int(id), data)
		return self.read(table, id=id)

	def delete(self, table, id):
		session = db.getDb(self.db_path+table+'.json')
		session.deleteById(int(id))
		return True