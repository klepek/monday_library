class Board:
	id=0
	name=""
	columns={}

	def AddColumn(self,column):
		# url /columns/numbers0/numeric.json
		columns[column['title']]={'id':column['id'], 'type':column['type'], 'raw':column, 'url':"/columns/"+str(column['id'])+"/"+str(column['type'])+".json"}

	def GetColumns(self):
		return self.columns

	def __init__(self,id):
		self.id=id