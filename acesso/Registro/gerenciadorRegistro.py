import sets
import psycopg2			#Conectar ao banco de dados

from apiSql.SqlInsert  import *
from apiSql.SqlSelect  import *
from apiSql.Criteria   import *
from apiSql.Filter     import *
#from apiSql.Connection import *

from registroAtividadeDocente import *

class GerenciadorRegistro:


	#def __init__(self):
		
	def inserirRegistro(self, registro):

		sql_insert  = SqlInsert()
		sql_select  = SqlSelect()
		conn = psycopg2.connect("host=localhost dbname=teste_dump user=postgres password=postgres")
		cursor = conn.cursor()

		
		
		# Obtemos todos os dados do CV Lattes	
		self.nomeCompleto                 = registro.nomeCompleto
		self.bolsaProdutividade           = registro.bolsaProdutividade
		self.enderecoProfissional         = registro.enderecoProfissional
		self.sexo                         = registro.sexo
		self.nomeEmCitacoesBibliograficas = registro.nomeEmCitacoesBibliograficas
		self.atualizacaoCV                = registro.atualizacaoCV
		self.textoResumo                  = registro.textoResumo
		self.foto                         = registro.foto

		self.listaIDLattesColaboradores = registro.listaIDLattesColaboradores
		self.listaFormacaoAcademica     = registro.listaFormacaoAcademica	
		self.listaAreaDeAtuacao         = registro.listaAreaDeAtuacao
		self.listaIdioma                = registro.listaIdioma
		self.listaPremioOuTitulo        = registro.listaPremioOuTitulo
		self.listaIDLattesColaboradoresUnica = sets.Set(self.listaIDLattesColaboradores)

		titulo = self.listaFormacaoAcademica[0].tipo	#Variavel temporaria.


		#Consultar registro do Professor
		criterio = Criteria()
		criterio.add(Filter('prof_nome', '=', sql_select.addSlashes(registro.nomeCompleto.encode('utf8'))))
		sql_select.setCriteria(criterio)
		cursor.execute(self.instructionSQL(sql_select, 'professor', ['prof_num_siape'], criterio))
		row = cursor.fetchone()

		if row is None:		
			cursor.execute("INSERT INTO professor (prof_nome, prof_titulacao, prof_vinculo) VALUES (%s, %s, %s)", (self.nomeCompleto, titulo, "Efetivo"))
			conn.commit()
		else:
			print "PROFESSOR JA REGISTRADO."


		#for item in registro.listaProjetoDePesquisa:
			#print item

	def instructionSQL(self, instruction, table, fields, values):

		if isinstance(instruction, SqlInsert):
			instruction.setTable(table)
			size_fields = len(fields)
			if isinstance(values, list) or isinstance(values, tuple):
				for item in range(size_fields):
					instruction.setRowData(fields[item], values[item])
				return instruction.getInstruction()

		elif isinstance(instruction, SqlSelect):
			instruction.setTable(table)
			size = len(fields)
			for item in range(size):
				instruction.addColumn(fields[item])
			if isinstance(values, Criteria):
				instruction.setCriteria(values)
			return instruction.getInstruction()
		else:		
			print 'NAO IMPLEMENTADO'
			
