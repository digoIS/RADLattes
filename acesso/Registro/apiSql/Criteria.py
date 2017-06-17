"""
Classe Criteria
Esta classe oferece uma interface para definir criterios de selecao compostos
"""
import string

from Expression import *


class Criteria(Expression):
	expression = None		#Armazena a lista de expressoes (objetos do tipo Expression)
	operators  = None		#Armazena a lista de operadores (AND, OR)
	properties = None		#Armazena a lista de propriedades do criterio (order by, offset, limit)

	"""
	metodo __init__()
	"""
	def __init__(self):
		'Instancia um novo criterio'
		self.expression = []		
		self.operators  = []		
		self.properties = {}
		
	"""
	metodo add()
	@param expression = expressao (objeto Expression)
	@param operator   = operador logico 
	"""
	def add(self, expression, operator = Expression.AND_OPERATOR):
		'Adiciona uma expressao ao criterio de selecao'
		if len(self.expression) == 0:
			operator = ''				#unset(operator)
		self.expression.append(expression)		#Agrega uma expressao a lista de expressoes
		self.operators.append(operator)			#Agraga o operador a lista de operadores

	"""
	metodo dump()
	"""
	def dump(self):
		'Retorna a expressao composta final'
		result = ''
		index = 0
		if isinstance(self.expression, list):
			for element in self.expression:
				operator = self.operators[index]
				result += operator+' '+element.dump() + ' '
				index = index + 1
			result = string.strip(result)
			return '(%s)' % (result)
	
	"""
	metodo setProperty()
	@param prop  = propriedade
	@param value = valor
	"""
	def setProperty(self, prop, value):
		'Define o valor de uma propriedade'
		self.properties[prop] = self.value

	"""
	metodo getProperty()
	@param prop = propriedade
	"""
	def getProperty(self, prop):
		'Retorna o valor da propriedade'
		keys = self.properties.keys()
		for element in keys:
			if prop == element:
				return self.properties[prop] 
		return ''
 
				


