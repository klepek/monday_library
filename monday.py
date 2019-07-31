from graphqlclient import GraphQLClient
import json
import time
from .pulse import Pulse
from .board import Board
from .exceptions import *

client = GraphQLClient('https://api.monday.com/v2')

class Monday(object):
	api_key = ""
	prod_board_id = 0
	boards = {}
	pulses = {}
	client= None

	def __init__(self, api_key):
		self.api_key=api_key
		self.client = GraphQLClient('https://api.monday.com/v2')
		self.client.inject_token(api_key)

	def query(self,ql,no=0):
		result = self.client.execute(ql)
		x = lambda:None
		x.__dict__ = json.loads(result)
		try:
			return x.data
		except AttributeError:
			# this could happen if we have either too complex query, or exceeded timeframe, try again with second delay
			if "exceeds max complexity" in x.errors[0]['message']:
				if (no==1):
					raise OverLimit("Error: "+str(x.errors[0]['message']))
				time.sleep(1)
				try:
					self.query(ql,1)
				except OverLimit:
					raise OverLimit("Error: "+str(x.errors[0]['message']))
			else:
				raise UnknownError("Error: "+str(x.errors[0]['message'])+" on ql "+ql)
		except Exception as ex:
			raise UnknownError("Error: "+str(x.errors[0]['message'])+" on ql "+ql)


	def GetAllPulse(self, board_id = None, groupFilter = None):
		if board_id is None:
			raise UnknownError("Missing board id")
		prod_board_id = board_id
		ql = "{boards(ids: "+str(prod_board_id)+") {groups {id title}}}"
		groups = "["
		return_data = []
		p = self.query(ql)
		for i in p['boards'][0]['groups']:
			if groupFilter is not None:
				if groupFilter in str(i['title']).lower():
					groups=groups+'"'+str(i['id'])+'",'
			else:
				groups=groups+'"'+str(i['id'])+'",'
		groups=groups[:-1]+"]"
		ql = "{boards(ids: "+str(prod_board_id)+") {groups (ids: "+groups+"){items {id}}}}"
		x = self.query(ql)
		for i in x['boards'][0]['groups']:
				for a in i['items']:
					return_data.append(a['id'])
		return return_data

	def GetPulse(self,id):
		try:
			value = self.pulses[id]
			return value
		except KeyError:
			ql = "{items(ids:"+str(id)+"){id name board {id}}}"
			result = self.client.execute(ql)
			x = lambda:None
			x.__dict__ = json.loads(result)
			pulse = Pulse(x.data['items'][0]['id'],x.data['items'][0]['name'],x.data['items'][0]['board']['id'])
			for i in self.GetBoardColumns(pulse.board_id):
				value = self.GetPulseColValue(pulse, i['id'], i['type'])
#				print("pulse.AddColumn("+str(i['id'])+", "+i['title']+", "+i['type']+","+str(value)+")")
				pulse.AddColumn(i['id'], i['title'], i['type'], value)
			self.pulses[pulse.id]=pulse
			return pulse

	def GetPulseColValue(self, pulse, column_id, column_type):
		# returns json value
		ql = '{items(ids:'+pulse.id+'){column_values(ids: "'+column_id+'"){value}}}'
#		print(ql)
		result = self.query(ql)
#		print(result['items'])
		data = lambda:None
		if not result['items'][0]['column_values']:
			return ""
		try:
			if ( result['items'][0]['column_values'][0]['value'] is None):
				return None
			data = json.loads(result['items'][0]['column_values'][0]['value'])
		except Exception:
			print(str(column_id)+" "+str(column_type))
		# lets see what we got
		if column_type=="link":
			try:
				return data['url']
			except:
				return result['items'][0]['column_values'][0]['value']
		if column_type=="email":
			try:
				return data['email']
			except:
				return result['items'][0]['column_values'][0]['value']
		if column_type=="color":
			try:
				return data['index']
			except:
				return result['items'][0]['column_values'][0]['value']
		return data

	def PutColumnValue(self, pulse, column_name, value):
		# did board change?
		testPulse = self.GetPulse(pulse.id)
		if testPulse.board_id != pulse.board_id:
			pulse=testPulse
		# validate that we have that column
		try:
			test = pulse.GetColumn(column_name)
		except ColumnNotFound:
			raise ColumnNotFound("Column "+column_name+" not found")
		json_value = json.dumps('"'+str(value)+'"')
		if (pulse.columns[column_name]['type'] == "link"):
			json_value=json.dumps(json.dumps({'url': value, 'text': value}))
		if (pulse.columns[column_name]['type'] == "color"):
			json_value=json.dumps(json.dumps({'label': value}))
		if (pulse.columns[column_name]['type'] == "email"):
			json_value=json.dumps(json.dumps({'email': value, 'text': value}))
		ql='mutation {change_column_value(item_id:'+pulse.id+', column_id:"'+pulse.columns[column_name]['id']+'",board_id:'+pulse.board_id+',value:'+json_value+') {id}} '
#		print(ql)
		self.query(ql)

	def GetBoardColumns(self,board_id):
		ql = "{boards(ids: "+str(board_id)+"){columns{id title type}}}"
		result = self.client.execute(ql)
		x = lambda:None
		x.__dict__ = json.loads(result)
		columns = []
		for i in x.data['boards'][0]['columns']:
			if i['id']=="name":
				continue
			else:
				columns.append(i)
		return columns

