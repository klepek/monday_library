import requests
from .pulse import Pulse
from .board import Board
from .exceptions import *

class Monday(object):
	monday_url = "https://api.monday.com:443/v1/"
	api_key = "api_key="
	api_key_end="?"+api_key
	boards = {}
	pulses = {}

	def __init__(self,api_key):
		self.api_key="api_key="+str(api_key)
		self.api_key_end="?"+self.api_key

	def GetPulse(self,id):
		#url = "https://api.monday.com:443/v1/pulses/"+str(id)+".json?api_key=..."
		url = self.monday_url+"/pulses/"+str(id)+self.api_key_end
		#print(url)
		r = requests.get(url)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code))
		data = r.json()
		pulse = Pulse(data['id'],data['name'],data['board_id'],data['url'])
		for i in self.GetBoardColumns(pulse.board_id):
			value = self.GetPulseColValue(pulse, i['id'])
			pulse.AddColumn(i['id'], i['title'], i['type'], value)
		self.pulses[pulse.id]=pulse
		return (pulse)

	def GetPulseColValue(self, pulse, column_id):
		# https://api.monday.com:443/v1/boards/board_id/columns/numbers0/value.json?pulse_id=pulse_id&return_as_array=true&api_key=...
		url = self.monday_url+"/boards/"+str(pulse.board_id)+"/columns/"+column_id+"/value.json?pulse_id="+str(pulse.id)+"&return_as_array=false&"+self.api_key
		#print(url)
		r = requests.get(url)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code))
		data = r.json()
		return data['value']

	def GetBoard(self, id):
		# https://api.monday.com:443/v1/boards/board_id.json?api_key=...
		raise NotImplemented("Not implemented")
		board=Board(id,name)
		return (board)

	def PutColumnValue(self, pulse, column_name, value):
		# TODO: verification of column
		# https://api.monday.com:443/v1/boards/board_id/columns/column_id/column_type.json?api_key=...
		# did board change?
		testPulse = self.GetPulse(pulse.id)
		if testPulse.board_id != pulse.board_id:
			pulse=testPulse
		# validate that we have that column
		try:
			test = pulse.GetColumn(column_name)
		except ColumnNotFound:
			raise ColumnNotFound("Column "+column_name+" not found")

		url = self.monday_url+"boards/"+str(pulse.board_id)+pulse.columns[column_name]['url']+self.api_key_end
		data={'pulse_id':pulse.id, 'value': value}
		#print(url)
		#print(data)
		r = requests.put(url, data)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code)+" url: "+url)

	def GetBoardColumns(self,board_id,archived=False):
		if archived:
			url = self.monday_url+"/boards/"+str(board_id)+"/columns.json?all_columns=true&"+self.api_key
		else:
			url = self.monday_url+"/boards/"+str(board_id)+"/columns.json?all_columns=false&"+self.api_key
		#print(url)
		r = requests.get(url)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code))
		data = r.json()
		return data

