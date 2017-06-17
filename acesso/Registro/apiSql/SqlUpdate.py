"""
"""
from appADO.SqlInstruction import SqlInstruction
import string

class SqlUpdate(SqlInstruction):
    columns = []        #Armazena as colunas
    values  = []        #Armazena os valores
    sql     = []        #Armazena a instrucao SQL

    """ 
    metodo setRowData()
    @param column: coluna da tabela
    @param value: valor a ser armazenado
    """
    def setRowData(self, column, value):
        'Atribui valores as colunas que serao inseridas no banco de dados'
        if isinstance(value, str) :
            value = self.addSlashes(value)        #Adicione o caracter de escape nas aspas
            self.setColumnValue(column, "'%s'" % (value))
        elif isinstance(value, bool) :
            if value:
                self.setColumnValue(column, 'TRUE')
            else: 
                self.setColumnValue(column, 'FALSE')
        elif value == None:
            self.setColumnValue(column, 'NULL')
        else:
            self.setColumnValue(column, str(value))

    """
    metodo getInstruction()
    """
    def getInstruction(self):
        'Retorna a instrucao UPDATE em forma de string plana'
        pairs = []
        delimiter = ', '
        index = 0
        self.sql = string.Template("""UPDATE $table SET $pairs WHERE $criteria""")
        if len(self.columns):
            for element in self.columns:
                pair = "%s = %s" % (element, self.values[index])
                pairs.append(pair)
                index = index + 1
        
        if self.criteria: 
            criteria = self.criteria
            
        dicToSubstitute = {'table': self.table, 'pairs': delimiter.join(pairs), 'criteria': criteria.dump()}
        return self.sql.substitute(dicToSubstitute)
        
        """
    metodo setColumnValue()
    @param column: coluna da tabela
    @param value: valor para coluna  
    """
    def setColumnValue(self, column, value):
        'Adiciona um valor a uma coluna da tabela'
        self.columns.append(column)
        self.values.append(value)