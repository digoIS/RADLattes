"""
Classe SqlSelect
Classe para manipular uma instrucao SELECT sobre o banco de dados
"""

import string

from SqlInstruction import *

class SqlSelect(SqlInstruction):
    columns = None
    
    def __init__(self):
        self.columns = []

    """
    metodo addColumn()
    adiciona uma coluna retornada pelo SELECT
    @param column: coluna da tabela 
    """
    def addColumn(self, column):
       	self.columns.append(column)
    
    """
    metodo getInstruction()
    retorna a instrucao SELECT na forma de string plana
    """
    
    def getInstruction(self):
        'Retorna a instrucao SELECT no formato de string plana'
        delimiter = ', '
        self.sql = string.Template("""SELECT $columns FROM $table WHERE $criterio $prop;""")
        strColumns = delimiter.join(self.columns)
        prop = ''
        if self.criteria:
            expression = self.criteria.dump()
            if expression:
                criterio = expression
            
            order  = self.criteria.getProperty('order')
            limit  = self.criteria.getProperty('limit')
            offset = self.criteria.getProperty('offset')
            
            if not order == '':
                prop += 'ORDER BY '+order
            if not limit == '':
                prop += ' LIMIT '+str(limit)
            if not offset == '':
                prop += ' OFFSET '+str(offset)
                
            dicToSubtitute = {'columns':strColumns, 'table':self.table, 'criterio':criterio, 'prop':prop}
	    self.clear()
            return self.sql.substitute(dicToSubtitute)

    def clear(self):
	self.columns = []
