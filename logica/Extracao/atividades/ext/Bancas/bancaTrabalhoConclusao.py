from bancas import *
class BancaTrabalhoConclusao(Bancas):
	alunos = None

	def __init__(self, idMembro, partesDoItem, nivel):
		Bancas.__init__(self, idMembro, nivel)
		# partesDoItem[0]: Numero (NAO USADO)
		# partesDoItem[1]: Descricao da banca (DADO BRUTO)		
		self.processaItem(partesDoItem[1])
		
	def processaItem(self, partesDoItem):
		#partes = partesDoItem.rpartition(" (")
		partes = partesDoItem.partition(" de ")
		lista = partes[2].split('.')

		#for item in lista:
			#print item	
		'''
		p2 = parte2.partition(' - ')
		curso = p2[0].rstrip('.')
		local = p2[2].strip().rstrip('.')
		self.local = local
		self.curso = curso
		
			partes = partes[0].rpartition(". ")
			if partes[1] == "":
				self.ano = ""
				partes = partes[0]
			else: 
				self.ano = partes[2]

			partes = partes[0].rpartition(".")
			if partes[1] == "":
				self.titulo = ""
				partes = partes[0].strip()
			else: 
				self.titulo = partes[2].strip()
				p = partes[0].partition("..")
				if p[1] == "":
					self.autores = partes[0]
					self.alunos = ""
				else:
					self.autores = p[0]
					alunos = p[2].split(',')
					if len(alunos) > 0:
						self.alunos = alunos
					else:
						self.alunos = p[2]'''

			
