import requests
from .pulse import Pulse
from .board import Board
from .exceptions import *

class Monday(object):
	monday_url = "https://api.monday.com:443/v1/"
	api_key = "api_key="
	api_key_end="?"+api_key

	def __init__(self,api_key):
		self.api_key="api_key="+str(api_key)
		self.api_key_end="?"+self.api_key

	def GetPulse(self,id):
		#url = "https://api.monday.com:443/v1/pulses/"+str(id)+".json?api_key=..."
		url = self.monday_url+"/pulses/"+str(id)+self.api_key_end
		print(url)
		r = requests.get(url)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code))
		data = r.json()
		pulse = Pulse(data['id'],data['name'],data['board_id'],data['url'])
		return (pulse)

	def GetBoard(self, id):
		#url = "https://api.monday.com:443/v1/..."
		raise NotImplemented("Not implemented")
		board=Board(id,name)
		return (board)

	def SetColumnValue(self, pulse, column_name, value):
		# TODO: verification of column
		# https://api.monday.com:443/v1/boards/board_id/columns/column_id/column_type.json?api_key=...	
		url = self.monday_url+"boards/"+str(pulse.board)+"/columns/"+pulse.column[column_name]['url']+self.api_key_end
		data={'pulse_id':pulse.id, 'value': value}
		#print(url)
		#print(data)
		r = requests.put(url, data)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code)+" url: "+url)

	def GetBoardColums(board,archived=False):
		if archived:
			url = self.monday_url+"/boards/"+str(board.id)+"/columns.json?all_columns=true"+self.api_key
		else:
			url = self.monday_url+"/boards/"+str(board.id)+"/columns.json"+self.api_key_end
		r = requests.get(url)
		if r.status_code != 200:
			raise AccessErrorException("Status code: "+str(r.status_code))
		data = r.json()
		for d in data:
			board.AddColumn(d)
		return (True)

	def GetPulseColumn(id, name):
		raise NotImplemented("Not implemented")
