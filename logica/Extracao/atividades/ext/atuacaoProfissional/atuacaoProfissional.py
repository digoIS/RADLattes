class AtuacaoProfissional:
	titulo = ''
	descricao = ''	
	periodo = ''


	def __str__(self):
        	s  = "\n[ATUACAO PROFISSIONAL] \n"
        	s += "+ TITULO         : " + str(self.descricao) + "\n"
        	s += "+ TIPO DO VINCULO: " + str(self.nivel) + "\n"
		s += "+ ENQUADRAMENTO  : " + str(self.nivel) + "\n"
        	return s
