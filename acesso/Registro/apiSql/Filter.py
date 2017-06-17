"""
Classe Filter
Essa classe oferece uma interface para criar filtros de selecao
"""

import string

from Expression import *
#from SqlInstruction import *

class Filter(Expression):#, SqlInstruction):

	variable = ''
	operator = ''
	value    = ''

	"""
	metodo __init__()
	@param variable: variavel
	@param operator: operador (<, >, =)
	@param value: valor para comparacao
	"""
	def __init__(self, variable, operator, value):
		'Instancia um novo filtro'
		self.variable = variable
		self.operator = operator
		#Transforma o valor em uma string plana
		self.value    = self.transform(value)

	"""
	metodo transform()
	@param value: valor a ser modificado
	"""
	def transform (self, value):	
		'Modifica os valores para serem interpretados corretamente pelo banco de dados'
		if isinstance(value, list):				#Verifica se e uma lista
			temp = []					#Lista temporaria
			#Percorre os valores da lista
			for element in value:
				if isinstance(element, int):
					intToStr = str(element) 	#Funcao join() espera str. Conversao de tipos: int -> str. 
					temp.append(intToStr)
				elif isinstance(element, str):
					#Adicionar as aspar se for string
					slashe_element = self.addSlashes(value)	
					print 'SLASHE ', slashe_element
					temp.append(slashe_element)
			result = '('+', '.join(temp)+')'		#Converte a lista temporaria em uma string separa por virgula ","
		elif isinstance(value, str):				#Verifica se e uma string	
			slashe_value = "'%s'" % (value)			#Armazena aspas
			result = slashe_value
		elif isinstance(value, bool):				#Verifica se e um booleano
			if value:					#Armazena TRUE ou FALSE
				result = 'TRUE'
			else:
				result = 'FALSE'
		elif value == None:					#Verifica se e um nulo
			result = 'NULL'					#Armazena NULL
		else:
			result = value
		return result

	""" 
	metodo dump()
	"""
	def dump(self):
		'Retorna o filtro no formato de uma expressao'
		expression = string.Template("""$variable $operator $value""")
		dic = {'variable': self.variable, 'operator': self.operator, 'value': self.value}
		return expression.safe_substitute(dic)	
		
	def addSlashes(self, s):
		'Adiciona os caracteres de escape'
		l = ["\\", "\"", "'", "\0"]
		for i in l:
			if i in s: 
				s = s.replace(i, "'"+i)
				print s
		return s
















 
