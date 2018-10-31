class Pulse:
	id = 0
	md_od = 0
	md_do = 0
	real_md = 0
	name = ""
	board=0

	def __init__(self,id, name, board, url):
		self.id=id
		self.name=name
		self.url=url
		self.board=board

	def setMDs(self, md_od, md_do):
		self.md_od=md_od
		self.md_do=md_do
	