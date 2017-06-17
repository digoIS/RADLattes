class ProducaoBibliografica:

	item 	 = None # dado bruto
	idMembro = None

	autores  = ''
	titulo 	 = ''
	ano 	 = ''

	volume 	 = ''
	paginas  = ''
	#Atributos para uso futuro
	doi      = None
	qualis   = None
	qualissimilar = None
	#Atributo auxiliar
	tipoProducao = ''.encode('utf8')
	def __init__ (self, tipo,  idMembro):
		self.idMembro = set([])
		self.idMembro.add(idMembro)
		self.tipoProducao = tipo
