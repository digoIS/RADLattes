from atuacaoProfissional import *
class Atividades(AtuacaoProfissional):
	cargo = ''
	orgao = ''
	listaInformacoes = ''

	def __init__(self, partesDoItem):
		listaInformacoes = []
		try:
			partes = partesDoItem.pop(0)
			self.periodo = partes[0]
			self.descricao = partes[1]
			self.cargo = partesDoItem.pop()		#Atributo na superclasse
		except:
			print "ERRO AO INICIALIZAR ATIVIDADES"
			pass

	def add(self, outrasInformacoes):
		try:
			self.listaInformacoes.append(outrasInformacoes)
		except:
			print "ERRO AO INSERIR OUTRAS INFORMACOES"
			pass
		
	def __str__(self):
        	s  = "\n[ATUACAO PROFISSIONAL - OUTRAS ATIVIDADES] \n"
		s += "+ PERIODO  : " + str(self.periodo) + "\n"
        	s += "+ CARGO    : " + str(self.cargo) + "\n"
        	s += "+ DESCRICAO: " + str(self.descricao) + "\n"
        	return s
