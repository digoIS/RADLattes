class Bancas:
	
	idMembro = None
	autores = None
	
	titulo = None
	local = None
	ano = None
	nivel = None

	def __init__(self, idMembro, nivel):	
		self.idMembro = set([])
		self.idMembro.add(idMembro)	
		self.nivel = nivel
			 	
	def __str__(self):
        	s  = "\n[PARTICIPACAO EM BANCAS] \n"
        	s += "+ TITULO     :" + str(self.titulo.encode('utf8'))+ "\n"
        	s += "+ ANO        :" + str(self.ano.encode('utf8')) + "\n"
		s += "+ LOCAL      :" + str(self.local.encode('utf8')) + "\n"
		s += "+ NIVEL      :" + str(self.nivel.encode('utf8')) + "\n"
        	return s		
		
