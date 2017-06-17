from atuacaoProfissional import *

class OutrasInformacoes(AtuacaoProfissional):
	descricao = ''
	
	def __init__(self, partesDoItem):
		#partesDoItem[0] = titulo
		#partesDoItem[1] = descricao
		try:
			self.titulo = partesDoItem[0]		
			self.descricao = partesDoItem[1]
			
		except:
			print "ERRO AO INICIALIZAR O OBJETO OUTRAS INFORMACOES."

	def __str__(self):
        	s  = "\n[ATUACAO PROFISSIONAL - OUTRAS INFORMACOES] \n"
        	s += "+ DESCRICAO: " + str(self.descricao) + "\n"
        	return s
