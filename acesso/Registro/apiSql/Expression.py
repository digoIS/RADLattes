"""
Classe Expression
Classe abstrata para gerenciar as expressoes de filtragem
"""
class Expression:
	#Operadores logicos
	AND_OPERATOR = 'AND'
	OR_OPERATOR  = 'OR'
	
	""" 
	metodo dump()
	@abstractmethod
	"""
	def dump(self):
		'Devera ser implementado em cada subclasse'
		raise NotImplementedError('Acao deve ser definida')
	
		
