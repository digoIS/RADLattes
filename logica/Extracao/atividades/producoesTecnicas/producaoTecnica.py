class ProducaoTecnica:

	item = None # dado bruto
	idMembro = None

	autores = None
	titulo = None
	ano = None
	tipo = None
	natureza = None

	def __init__(self, idMembro, tipo):
		self.idMembro = set([])
		self.idMembro.add(idMembro)
		self.tipo = tipo
