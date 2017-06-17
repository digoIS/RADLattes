#!/usr/bin/python
# encoding: utf-8
from formacaoAcademica import *

from idioma import *
from premioOuTitulo import *
from projetoDePesquisa import *

from artigoEmPeriodico import *
from livroPublicado import *
from capituloDeLivroPublicado import *
from textoEmJornalDeNoticia import *
from trabalhoCompletoEmCongresso import *
from resumoExpandidoEmCongresso import *
from resumoEmCongresso import *
from artigoAceito import *
from apresentacaoDeTrabalho import *
from outroTipoDeProducaoBibliografica import *

from softwareComPatente import *
from softwareSemPatente import *
from produtoTecnologico import *
from processoOuTecnica import *
from trabalhoTecnico import *
from outroTipoDeProducaoTecnica import *
from producaoArtistica import *

from orientacaoEmAndamento import *
from orientacaoConcluida import *

from organizacaoDeEvento import *
from participacaoEmEvento import *

########NOVAS LISTAS############
#Atuacao profissional
from atuacaoProfissional import *
from vinculoFuncional import *
from outrasInformacoes import *
#Bancas
from bancaTrabalhoConclusao import *
from bancaConcurso import *

class RegistroAtividadeDocente:

	idLattes = None # ID Lattes
	idMembro = None
	# Informacoes pessoais
	nomeInicial  = ''
	nomeCompleto = ''
	sexo 	     = ''
	nomeEmCitacoesBibliograficas = ''
	enderecoProfissional 	     = ''
	bolsaProdutividade 	     = ''
	textoResumo 		     = ''
	foto 			     = ''
	atualizacaoCV = ''

	# Lista informacoes ligadas a pessoa:
	listaFormacaoAcademica 	= None
	listaAreaDeAtuacao 	= None
	listaIdioma 		= None
	listaPremioOuTitulo 	= None
	listaIDLattesColaboradores 	= None
	listaIDLattesColaboradoresUnica = None

	# Projetos de pesquisa
	listaProjetoDePesquisa = None
	
	listaArtigoEmPeriodico 			= None
	listaLivroPublicado 			= None
	listaCapituloDeLivroPublicado 		= None
	listaTextoEmJornalDeNoticia 		= None
	listaTrabalhoCompletoEmCongresso	= None
	listaResumoExpandidoEmCongresso 	= None
	listaResumoEmCongresso 			= None
	listaArtigoAceito 			= None
	listaApresentacaoDeTrabalho 		= None
	listaOutroTipoDeProducaoBibliografica = None

	# Producao tecnica
	listaSoftwareComPatente = None		
	listaSoftwareSemPatente = None		
	listaProdutoTecnologico = None		
	listaProcessoOuTecnica 	= None		
	listaTrabalhoTecnico 	= None		
	listaOutroTipoDeProducaoTecnica = None	

	# Producao artistica/cultural
	listaProducaoArtistica = None		

	# Orientacoes em andamento
	listaOASupervisaoDePosDoutorado   = None	
	listaOATeseDeDoutorado 		  = None
	listaOADissertacaoDeMestrado 	  = None
	listaOAMonografiaDeEspecializacao = None
	listaOATCC 			  = None
	listaOAIniciacaoCientifica 	  = None
	listaOAOutroTipoDeOrientacao 	  = None

	# Orientacoes concluidas
	listaOCSupervisaoDePosDoutorado   = None	
	listaOCTeseDeDoutorado 		  = None		
	listaOCDissertacaoDeMestrado 	  = None	
	listaOCMonografiaDeEspecializacao = None	
	listaOCTCC 			  = None			
	listaOCIniciacaoCientifica 	  = None	
	listaOCOutroTipoDeOrientacao 	  = None

	# Eventos
	listaParticipacaoEmEvento = None	
	listaOrganizacaoDeEvento  = None		

	#Bancas
	listaBancaConcurso 	    = None
	listaBancaTrabalhoConclusao = None

	#Logica para criar o registro
	def __init__ (self, idMembro):
		self.idMembro = idMembro
		self.sexo = 'Masculino'

		self.listaIDLattesColaboradores = []
		self.listaFormacaoAcademica = []
		self.listaProjetoDePesquisa = []
		self.listaAreaDeAtuacao = []
		self.listaIdioma = []
		self.listaPremioOuTitulo = []

		self.listaArtigoEmPeriodico = []
		self.listaLivroPublicado = []
		self.listaCapituloDeLivroPublicado = []
		self.listaTextoEmJornalDeNoticia = []
		self.listaTrabalhoCompletoEmCongresso = []
		self.listaResumoExpandidoEmCongresso = []
		self.listaResumoEmCongresso = []
		self.listaArtigoAceito = []
		self.listaApresentacaoDeTrabalho = []
		self.listaOutroTipoDeProducaoBibliografica = []

		self.listaSoftwareComPatente = []
		self.listaSoftwareSemPatente = []
		self.listaProdutoTecnologico = []
		self.listaProcessoOuTecnica = []
		self.listaTrabalhoTecnico = []
		self.listaOutroTipoDeProducaoTecnica = []
		self.listaProducaoArtistica = []

		self.listaOASupervisaoDePosDoutorado = []
		self.listaOATeseDeDoutorado = []
		self.listaOADissertacaoDeMestrado = []
		self.listaOAMonografiaDeEspecializacao = []
		self.listaOATCC = []
		self.listaOAIniciacaoCientifica = []
		self.listaOAOutroTipoDeOrientacao = []

		self.listaOCSupervisaoDePosDoutorado = []
		self.listaOCTeseDeDoutorado = []
		self.listaOCDissertacaoDeMestrado = []
		self.listaOCMonografiaDeEspecializacao = []
		self.listaOCTCC = []
		self.listaOCIniciacaoCientifica = []
		self.listaOCOutroTipoDeOrientacao = []

		self.listaParticipacaoEmEvento = []
		self.listaOrganizacaoDeEvento = []

		self.listaBancaTrabalhoConclusao = []
		self.listaBancaConcurso = []

	def defineNomeInicial(self, nome):
		self.nomeInicial = nome 
	def defineNomeCompleto(self, nomeCompleto):
		self.nomeCompleto = nomeCompleto
	def defineSexo(self, sexo):
		self.sexo = sexo
	def defineEnderecoProfissional(self, endereco):
		self.enderecoProfissional = endereco
	def defineTextoResumo(self, textoResumo):
		self.textoResumo = textoResumo
	def defineNomeCitacoes(self, nomeCitacoes):
		self.nomeEmCitacoesBibliograficas = nomeCitacoes
	def defineBolsaProdutividade(self, bolsaProdutividade):
		self.bolsaProdutividade = bolsaProdutividade
	def defineDataAtualizacaoCV(self, data):
		self.atualizacaoCV = data
	













