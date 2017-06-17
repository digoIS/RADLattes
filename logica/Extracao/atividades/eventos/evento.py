class Evento:

	item = None # dado bruto
	idMembro = []

	nomeDoEvento = None
	natureza = None
	ano = None
	tipo = None

	def __init__(self, idMembro, tipo):
		self.idMembro = set([])
		self.idMembro.add(idMembro)
		self.tipo = tipo
