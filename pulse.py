class Pulse:
	id = 0
	name = ""
	board_id=0
	columns = {}

	def __init__(self,id, name, board_id, url):
		self.id=id
		self.name=name
		self.url=url
		self.board_id=board_id

	def AddColumn(self, column_id, column_name, column_type, value):
		self.columns[column_name] = {
				'id': column_id,
				'name': column_name,
				'type': column_type,
				'url': "/columns/"+str(column_id)+"/"+column_type+".json",
				'value':value,
				}

	def GetColumn(self, column_name):
		try:
			return self.columns[column_name]
		except AttributeError:
			raise ColumnNotFound("column "+column_name+" does not exists")


	def GetColumnValue(self, column_name):
		try:
			return self.columns[column_name]['value']
		except AttributeError:
			raise AttributeError("value not found for column "+column_name)