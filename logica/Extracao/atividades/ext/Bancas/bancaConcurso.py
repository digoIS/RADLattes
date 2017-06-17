from bancas import *
class BancaConcurso(Bancas):
	
	def __init__(self, idMembro, partesDoItem, nivel):
		Bancas.__init__(self, idMembro, nivel)
		self.processaItem(partesDoItem)

	def processaItem(self, partesDoItem):
		partes = partesDoItem[1].rpartition(". ")
		if partes[1] == "":
			self.local = ""
			partes = partes[0]
		else:
			self.local = partes[2].strip().rstrip(".")
			partes = partes[0].rpartition(". ")
			if partes[1] == "":
				self.ano = ""
				partes = partes[0]
			else: 
				self.ano = partes[2]

			partes = partes[0].rpartition(". ")
			if partes[1] == "":
				self.titulo = ""
				partes = partes[0].strip()
			else: 
				self.titulo = partes[2].strip()
				self.autores = partes[0]
