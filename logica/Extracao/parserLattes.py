#!/usr/bin/python
# encoding: utf-8
# filename: parserLattes.py
#
#  scriptLattes V8
#  Copyright 2005-2013: Jesús P. Mena-Chalco e Roberto M. Cesar-Jr.
#  http://scriptlattes.sourceforge.net/
#
#
#  Este programa é um software livre; você pode redistribui-lo e/ou 
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como 
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da 
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util, 
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
import HTMLParser
import re
import string
from tidylib import tidy_document
from htmlentitydefs import name2codepoint
# ---------------------------------------------------------------------------- #
from HTMLParser import HTMLParser
#from curriculoVitae import *
from registroAtividadeDocente import *

#ControladorExtracao:
class ParserLattes(HTMLParser):
	
	identificador16 = ''
	item = None
	salvarIdentificador16 = None
	# Dados Gerais
	salvarNome = None
	salvarNomeEmCitacoes = None
	salvarSexo = None
	salvarTextoResumo = None
	salvarEnderecoProfissional = None
	salvarProjetoDePesquisa = None
	salvarAreaDeAtuacao = None
	salvarIdioma = None
	salvarPremioOuTitulo = None
	salvarFormacaoAcademica = None
	# Fim Dados Gerais

	salvarBolsaProdutividade = None
	salvarParticipacaoEmEvento = None
	salvarOrganizacaoDeEvento = None
	salvarBancas = None

	salvarAtualizacaoCV = None
	salvarItem = None
	# novos atributos
	achouIdentificacao = None
	achouEndereco = None
	salvarParte1 = None
	salvarParte2 = None
	salvarParte3 = None

	achouProducoes = None
	achouProducaoEmCTA = None
	achouProducaoTecnica = None
	achouProducaoArtisticaCultural = None
	achouOutraProducaoArtisticaCultural = None

	achouBancas = None
	achouEventos = None
	achouOrientacoes = None
	achouOutrasInformacoesRelevantes = None
	achouDemaisTrabalho = None
	achouFormacaoComplementar = None	
	spanInformacaoArtigo = None

	recuperarIdentificador16 = None

	achouAtuacaoProfissional = None
	achouVinculoInstitucional = None
	achouOutrasInformacoes = None

	achoArtesCenicas = None
	achouMusica = None	
	achouAtividades = None

	#Bancas
	achouBancaQualificacaoDoutorado = None
	achouBancaQualificacaoMestrado = None
	achouBancaAperfeicoamentoEspecializacao = None
	achouBancaMestrado = None
	achouBancaTCC = None
	achouBancaCP = None
	achouBancaOP = None
	achouBancaTC = None
	achouBancaCJ = None
	achouBancaAC = None

	achouGrupo = None
	achouEnderecoProfissional = None
	achouSexo = None
	achouNomeEmCitacoes = None
	achouFormacaoAcademica = None
	achouProjetoDePesquisa = None
	achouAreaDeAtuacao = None
	achouIdioma = None
	achouPremioOuTitulo = None

	achouArtigoEmPeriodico = None
	achouLivroPublicado = None
	achouCapituloDeLivroPublicado = None
	achouTextoEmJornalDeNoticia = None
	achouTrabalhoCompletoEmCongresso = None
	achouResumoExpandidoEmCongresso = None
	achouResumoEmCongresso = None
	achouArtigoAceito = None
	achouApresentacaoDeTrabalho = None
	achouOutroTipoDeProducaoBibliografica = None

	achouSoftwareComPatente = None
	achouSoftwareSemPatente = None
	achouProdutoTecnologico = None
	achouProcessoOuTecnica = None
	achouTrabalhoTecnico = None
	achouOutroTipoDeProducaoTecnica = None
	achouProducaoArtistica = None

	achouOrientacoesEmAndamento	= None
	achouOrientacoesConcluidas = None
	achouSupervisaoDePosDoutorado = None
	achouTeseDeDoutorado = None
	achouDissertacaoDeMestrado = None
	achouMonografiaDeEspecializacao = None
	achouTCC = None
	achouIniciacaoCientifica = None
	achouOutroTipoDeOrientacao = None

	achouParticipacaoEmEvento = None
	achouOrganizacaoDeEvento = None

	procurarCabecalho = None
	partesDoItem = []

	# auxiliares
	doi = ''
	relevante = 0
	umaUnidade = 0
	idOrientando = None
	
	registro = None		# Registro com as Atividades Academicas do Docente.
	# ------------------------------------------------------------------------ #
	def __init__(self, idMembro, cvLattesHTML):
		HTMLParser.__init__(self)
		# Curriculo - inicializacao obrigatoria
		self.registro = RegistroAtividadeDocente(idMembro)
		self.idMembro = idMembro
		# Inicializacao para evitar a busca exaustiva de algumas palavras-chave
		self.salvarAtualizacaoCV = 1 
		self.salvarFoto = 1
		self.procurarCabecalho = 0
		self.achouGrupo = 0
		self.doi = ''
		self.relevante = 0
		self.idOrientando = ''
		self.item = ''
		# Alimenta o Parser o arquivo HTML
		self.feed(cvLattesHTML)
	# ------------------------------------------------------------------------ #
	def obterRegistroAtividades(self):
		return self.registro

	def handle_starttag(self, tag, attributes):

		if tag=='h2':
			for name, value in attributes:
				if name=='class' and value=='nome':
					self.salvarNome = 1
					self.item = ''
					break
		if tag=='li':
		    self.recuperarIdentificador16 = 1
		# <p class=resumo> </p>
		if tag=='p':
			for name, value in attributes:
				if name=='class' and value=='resumo':
					self.salvarTextoResumo = 1
					self.item = ''
					break

		if (tag=='br' or tag=='img') and self.salvarNome:
			self.nomeCompleto = stripBlanks(self.item)
			# self.curriculoVitae.DadosGerais.addNomeCompleto(stripBlanks(self.item))
			self.registro.defineNomeCompleto(stripBlanks(self.item))
			self.item = ''
			self.salvarNome = 0
			self.salvarBolsaProdutividade = 1

		if tag=='span' and self.salvarBolsaProdutividade:
			self.item = ''

		if tag=='div':

			#Dados que estao marcados com <div class='title-wrapper'></div>
			# Encontrou uma secao
			for name, value in attributes:
				if name=='class' and value=='title-wrapper':
					self.umaUnidade = 1	
					break
			
			#Dados que estao marcados com <div class='layout-cell-pad-5'>VALOR</div> sao os valores dos campos
			for name, value in attributes:
				if name=='class' and value=='layout-cell-pad-5':
					# Se o campo foi encontrado na secao Identificacao
					if self.achouNomeEmCitacoes:
						self.salvarNomeEmCitacoes = 1
						self.item = ''

					if self.achouSexo:
						self.salvarSexo = 1
						self.item = ''

					if self.achouEnderecoProfissional:
						self.salvarEnderecoProfissional = 1
						self.item = ''

					if self.salvarParte1:
						self.salvarParte1 = 0
						self.salvarParte2 = 1
				#Dados que estao marcados com <div class='layout-cell-pad-5 text-align-right'></div>
				if name=='class' and value=='layout-cell-pad-5 text-align-right':
					self.item = ''
					if self.achouFormacaoAcademica or self.achouAtuacaoProfissional or self.achouProjetoDePesquisa or self.achouMembroDeCorpoEditorial or self.achouRevisorDePeriodico or self.achouAreaDeAtuacao or self.achouIdioma or self.achouPremioOuTitulo or self.salvarItem: 
						self.salvarParte1 = 1
						self.salvarParte2 = 0
						if not self.salvarParte3:
							self.partesDoItem = []

		# Encontrou o cabecalho da secao: tag h1 dentro de uma div da classe title-wrapper
		if tag=='h1' and self.umaUnidade: 
			self.procurarCabecalho = 1		# Encontrar o titulo do cabecalho

			self.achouIdentificacao = 0
			self.achouEndereco = 0
			self.achouFormacaoAcademica = 0
			self.achouAtuacaoProfissional = 0
			self.achouProjetoDePesquisa = 0
			self.achouMembroDeCorpoEditorial = 0
			self.achouRevisorDePeriodico = 0
			self.achouAreaDeAtuacao = 0
			self.achouIdioma = 0
			self.achouPremioOuTitulo = 0
			self.achouProducoes = 0
			self.achouProducaoEmCTA = 0
			self.achouProducaoTecnica = 0
			self.achouProducaoArtisticaCultural = 0
			self.achouBancas = 0
			self.achouEventos = 0
			self.achouOrientacoes = 0
			self.achouOutrasInformacoesRelevantes = 0
			self.achouDemaisTrabalhos = 0			
			self.salvarItem = 0
			
		if tag=='img':
			if self.salvarFoto: 
				for name, value in attributes:
					if name=='src' and u'servletrecuperafoto' in value:
						self.foto = value
						self.salvarFoto = 0
						break

			if self.salvarItem:
				for name, value in attributes:
					if name=='src' and u'ico_relevante' in value:
						self.relevante = 1
						break

		if tag=='br':
			self.item = self.item + ' '
		
		if tag=='span':
			if self.achouProducaoEmCTA:
				for name, value in attributes:
					if name=='class' and value==u'informacao-artigo':
						self.spanInformacaoArtigo = 1
		
		if tag=='a':
			if self.salvarItem: # and self.achouArtigoEmPeriodico:
				for name, value in attributes:
					if name=='href' and u'doi' in value:
						self.doi = value
						break

					id = re.findall(u'http://lattes.cnpq.br/(\d{16})', value)
					if name=='href' and len(id)>0:
						self.registro.listaIDLattesColaboradores.append(id[0])
						if self.achouOrientacoesEmAndamento or self.achouOrientacoesConcluidas:
							self.idOrientando = id[0]
						break


	# ------------------------------------------------------------------------ #
	def handle_endtag(self, tag):
		# Informações do pesquisador (pre-cabecalho)
		if tag=='h2':
			if self.salvarNome:
				#self.curriculoVitae.DadosGerais.addNomeCompleto(stripBlanks(self.item))
 				self.nomeCompleto = stripBlanks(self.item)
				self.registro.defineNomeCompleto(stripBlanks(self.item))
				self.salvarNome = 0
			if self.salvarBolsaProdutividade:
				self.salvarBolsaProdutividade = 0

		if tag=='p':
			if self.salvarTextoResumo:
				#self.curriculoVitae.DadosGerais.addTextoResumo(stripBlanks(self.item))
				self.textoResumo = stripBlanks(self.item)
				self.registro.defineTextoResumo(self.textoResumo)
				self.salvarTextoResumo = 0

		if tag=='span' and self.salvarBolsaProdutividade:
			self.bolsaProdutividade = stripBlanks(self.item)
			self.bolsaProdutividade = re.sub('Bolsista de Produtividade em Pesquisa do CNPq - ','', self.bolsaProdutividade)
			self.bolsaProdutividade = self.bolsaProdutividade.strip('()')
			self.registro.defineBolsaProdutividade(self.bolsaProdutividade)
			self.salvarBolsaProdutividade = 0
		
		if tag=='span' and self.salvarIdentificador16 == 1:
			self.identificador16 = re.findall(u'http://lattes.cnpq.br/(\d{16})', value)
			self.salvarIdentificador16 = 0
			
		# Resetar a flag para continuar a busca
		if tag=='h1' and self.procurarCabecalho:
			self.procurarCabecalho = 0


		if tag=='div': 
			if self.salvarNomeEmCitacoes:
				#self.curriculoVitae.DadosGerais.addNomeCitacoes(stripBlanks(self.item))
				self.nomeEmCitacoesBibliograficas = stripBlanks(self.item)
				self.registro.defineNomeCitacoes(self.nomeEmCitacoesBibliograficas)
				self.salvarNomeEmCitacoes = 0
				self.achouNomeEmCitacoes = 0
			if self.salvarSexo:
				#self.curriculoVitae.DadosGerais.addSexo(stripBlanks(self.item))
				self.sexo = stripBlanks(self.item)
				self.registro.defineSexo(self.sexo)
				self.salvarSexo = 0
				self.achouSexo = 0
			if self.salvarEnderecoProfissional:
				#self.curriculoVitae.DadosGerais.addTextoResumo(stripBlanks(self.item))
				self.enderecoProfissional = stripBlanks(self.item)
				self.enderecoProfissional = re.sub("\'", '', self.enderecoProfissional)
				self.enderecoProfissional = re.sub("\"", '', self.enderecoProfissional)
				self.registro.defineEnderecoProfissional(self.enderecoProfissional)
				self.salvarEnderecoProfissional = 0
				self.achouEnderecoProfissional = 0
			
			if (self.salvarParte1 and not self.salvarParte2) or (self.salvarParte2 and not self.salvarParte1) :
				if len(stripBlanks(self.item))>0:
					self.partesDoItem.append(stripBlanks(self.item)) # acrescentamos cada celula da linha em uma lista!
					self.item = ''

				if self.salvarParte2:
					self.salvarParte1 = 0
					self.salvarParte2 = 0

					if self.achouFormacaoAcademica and len(self.partesDoItem)>=2:
						##self.curriculoVitae.DadosGerais.addFormacaoAcademica(stripBlanks(self.item))
						iessimaFormacaoAcademica = FormacaoAcademica(self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.registro.listaFormacaoAcademica.append(iessimaFormacaoAcademica) # acrescentamos o objeto de FormacaoAcademica

					if self.achouAtuacaoProfissional:
						if self.achouVinculoInstitucional:
							if len(self.partesDoItem) > 1:
								iessimoVinculo = VinculoFuncional(self.partesDoItem)
								#print iessimoVinculo.showData()				
								#iessimoVinculo.add(self.partesDoItem)
												
						'''if self.achouAtividades:
							print self.partesDoItem
							iessimaAtividade = Atividades(self.partesDoItem)
							iessimoVinculo.add

						if self.achouOutrasInformacoes:
							print self.partesDoItem
							iessimaInformacao = OutrasInformacoes(self.partesDoItem)'''
				
					if self.achouProjetoDePesquisa:
						if not self.salvarParte3:
							self.salvarParte3 = 1
						else:
							self.salvarParte3 = 0
							if len(self.partesDoItem)>=3:
								iessimoProjetoDePesquisa = ProjetoDePesquisa(self.idMembro, self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
								self.registro.listaProjetoDePesquisa.append(iessimoProjetoDePesquisa) # acrescentamos o objeto de ProjetoDePesquisa

					'''if self.achouMembroDeCorpoEditorial:
						for membro in self.partesDoItem:
							print 'CORPO EDITORIAL', membro

					if self.achouRevisorDePeriodico:
						for membro in self.partesDoItem:
							print 'REVISOR PERIODICO:', membro'''
					
					if self.achouIdioma and len(self.partesDoItem)>=2:
						iessimoIdioma = Idioma(self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.registro.listaIdioma.append(iessimoIdioma) # acrescentamos o objeto de Idioma

					if self.achouPremioOuTitulo and len(self.partesDoItem)>=2:
						iessimoPremio = PremioOuTitulo(self.idMembro, self.partesDoItem) # criamos um objeto com a lista correspondentes às celulas da linha
						self.registro.listaPremioOuTitulo.append(iessimoPremio) # acrescentamos o objeto de PremioOuTitulo

					if self.achouProducoes:
						tipo = ''
						if self.achouProducaoEmCTA:
							if self.achouArtigoEmPeriodico:
								tipo = 'AP'
 	 							iessimoItem = ArtigoEmPeriodico(self.idMembro, tipo, self.partesDoItem, self.doi)
								self.registro.listaArtigoEmPeriodico.append(iessimoItem)
								self.doi = ''

							if self.achouLivroPublicado:
								tipo = 'LP'
	 	 						iessimoItem = LivroPublicado(self.idMembro, tipo, self.partesDoItem)
								self.registro.listaLivroPublicado.append(iessimoItem)
		
							if self.achouCapituloDeLivroPublicado:
								tipo = 'CLP'
		 						iessimoItem = CapituloDeLivroPublicado(self.idMembro, tipo,  self.partesDoItem)
								self.registro.listaCapituloDeLivroPublicado.append(iessimoItem)
												
							if self.achouTextoEmJornalDeNoticia:
								tipo = 'TJN'
 		 						iessimoItem = TextoEmJornalDeNoticia(self.idMembro, tipo,  self.partesDoItem)
								self.registro.listaTextoEmJornalDeNoticia.append(iessimoItem)
					
							if self.achouTrabalhoCompletoEmCongresso:
								tipo = 'TCC'
 	 							iessimoItem = TrabalhoCompletoEmCongresso(self.idMembro, tipo, self.partesDoItem, self.doi)
								self.registro.listaTrabalhoCompletoEmCongresso.append(iessimoItem)
								self.doi = ''
													
							if self.achouResumoExpandidoEmCongresso:
								tipo = 'REC'
 	 							iessimoItem = ResumoExpandidoEmCongresso(self.idMembro, tipo,  self.partesDoItem, self.doi)
								self.registro.listaResumoExpandidoEmCongresso.append(iessimoItem)
								self.doi = ''
												
							if self.achouResumoEmCongresso:
								tipo = 'RC'
 		 						iessimoItem = ResumoEmCongresso(self.idMembro, tipo, self.partesDoItem, self.doi)
								self.registro.listaResumoEmCongresso.append(iessimoItem)
								self.doi = ''
								
							if self.achouArtigoAceito:
								tipo = 'AA'
 		 						iessimoItem =  ArtigoAceito(self.idMembro, tipo, self.partesDoItem, self.doi)
								self.registro.listaArtigoAceito.append(iessimoItem)
								self.doi = ''
					
							if self.achouApresentacaoDeTrabalho:
								tipo = 'AT'
 		 						iessimoItem =  ApresentacaoDeTrabalho(self.idMembro, tipo, self.partesDoItem)
								self.registro.listaApresentacaoDeTrabalho.append(iessimoItem)
    
							if self.achouOutroTipoDeProducaoBibliografica:
								tipo = 'OTPB'
 		 						iessimoItem = OutroTipoDeProducaoBibliografica(self.idMembro, tipo, self.partesDoItem)
								self.registro.listaOutroTipoDeProducaoBibliografica.append(iessimoItem)


						if self.achouProducaoTecnica:
							if self.achouSoftwareComPatente:
 	 							iessimoItem = SoftwareComPatente(self.idMembro, self.partesDoItem, 'PCCR')
								self.registro.listaSoftwareComPatente.append(iessimoItem)
    
							if self.achouSoftwareSemPatente:
 	 							iessimoItem = SoftwareSemPatente(self.idMembro, self.partesDoItem, 'PCSR')							
								self.registro.listaSoftwareSemPatente.append(iessimoItem)
						
							if self.achouProdutoTecnologico:
 	 							iessimoItem = ProdutoTecnologico(self.idMembro, self.partesDoItem, 'PDT')
								self.registro.listaProdutoTecnologico.append(iessimoItem)
    
							if self.achouProcessoOuTecnica:
 	 							iessimoItem = ProcessoOuTecnica(self.idMembro, self.partesDoItem, 'PCT')
								self.registro.listaProcessoOuTecnica.append(iessimoItem)
    
							if self.achouTrabalhoTecnico:
 	 							iessimoItem = TrabalhoTecnico(self.idMembro, self.partesDoItem, 'TT')
								self.registro.listaTrabalhoTecnico.append(iessimoItem)
    
							if self.achouOutroTipoDeProducaoTecnica:
 	 							iessimoItem = OutroTipoDeProducaoTecnica(self.idMembro, self.partesDoItem,'OTPT')
								self.registro.listaOutroTipoDeProducaoTecnica.append(iessimoItem)

						if self.achouProducaoArtisticaCultural:
							if self.achouOutraProducaoArtisticaCultural:
 								iessimoItem = ProducaoArtistica(self.idMembro, self.partesDoItem, self.relevante, 'OTPA')
								self.registro.listaProducaoArtistica.append(iessimoItem)
							if self.achouArtesCenicas:
								print 'ACHOU ARTES CENICAS'
							if self.achouMusica:
								print 'ACHOU MUSICA'

					if self.achouBancas:
						if self.achouBancaTC:
							if self.achouBancaQualificacaoDoutorado:
								iessima = BancaTrabalhoConclusao(self.idMembro, self.partesDoItem, 'Qualificacao Doutorado')
								self.registro.listaBancaTrabalhoConclusao.append(iessima)
							if self.achouBancaQualificacaoMestrado:
								iessima = BancaTrabalhoConclusao(self.idMembro, self.partesDoItem, 'Qualificacao Mestrado')
								self.registro.listaBancaTrabalhoConclusao.append(iessima)
							if self.achouBancaAperfeicoamentoEspecializacao:
								iessima = BancaTrabalhoConclusao(self.idMembro, self.partesDoItem, 'Aperfeicoamento/Especializacao')
								self.registro.listaBancaTrabalhoConclusao.append(iessima)	
							if self.achouBancaMestrado:
								iessima = BancaTrabalhoConclusao(self.idMembro, self.partesDoItem, 'Mestrado')
								self.registro.listaBancaTrabalhoConclusao.append(iessima)
							if self.achouBancaTCC:
								iessima = BancaTrabalhoConclusao(self.idMembro, self.partesDoItem, 'Graduacao')
								self.registro.listaBancaTrabalhoConclusao.append(iessima)

						if self.achouBancaCJ:
							if self.achouBancaCP:
								iessima = BancaConcurso(self.idMembro, self.partesDoItem, 'Concurso')
								self.registro.listaBancaConcurso.append(iessima)
							if self.achouBancaOP:
								iessima = BancaConcurso(self.idMembro, self.partesDoItem, 'Outras')
								self.registro.listaBancaConcurso.append(iessima)
							if self.achouBancaAC:
								iessima = BancaConcurso(self.idMembro, self.partesDoItem, 'Avaliacao')
								self.registro.listaBancaConcurso.append(iessima)

					#if self.achouDemaisTrabalho:
					if self.achouEventos:
						if self.achouParticipacaoEmEvento:
							self.registro.listaParticipacaoEmEvento.append(ParticipacaoEmEvento(self.idMembro, 'PE', self.partesDoItem))
						if self.achouOrganizacaoDeEvento:
							self.registro.listaOrganizacaoDeEvento.append(OrganizacaoDeEvento(self.idMembro, 'OE', self.partesDoItem))


					if self.achouOrientacoes:
						if self.achouOrientacoesEmAndamento:
							if self.achouSupervisaoDePosDoutorado:
								self.registro.listaOASupervisaoDePosDoutorado.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTeseDeDoutorado:
								self.registro.listaOATeseDeDoutorado.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouDissertacaoDeMestrado:
								self.registro.listaOADissertacaoDeMestrado.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouMonografiaDeEspecializacao:
								self.registro.listaOAMonografiaDeEspecializacao.append( OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTCC:
								self.registro.listaOATCC.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouIniciacaoCientifica:
								self.registro.listaOAIniciacaoCientifica.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouOutroTipoDeOrientacao:
								self.registro.listaOAOutroTipoDeOrientacao.append(OrientacaoEmAndamento(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''

						if self.achouOrientacoesConcluidas :
							if self.achouSupervisaoDePosDoutorado:
								self.registro.listaOCSupervisaoDePosDoutorado.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTeseDeDoutorado:
								self.registro.listaOCTeseDeDoutorado.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouDissertacaoDeMestrado:
								self.registro.listaOCDissertacaoDeMestrado.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouMonografiaDeEspecializacao:
								self.registro.listaOCMonografiaDeEspecializacao.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouTCC:
								self.registro.listaOCTCC.append( OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouIniciacaoCientifica:
								self.registro.listaOCIniciacaoCientifica.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''
							if self.achouOutroTipoDeOrientacao:
								self.registro.listaOCOutroTipoDeOrientacao.append(OrientacaoConcluida(self.idMembro, self.partesDoItem, self.idOrientando) )
								self.idOrientando = ''


		if tag=='span':
			if self.spanInformacaoArtigo:
				self.spanInformacaoArtigo = 0


	# ------------------------------------------------------------------------ #
	def handle_data(self, dado):
		if not self.spanInformacaoArtigo:
			self.item = self.item + htmlentitydecode(dado)
			
		dado = stripBlanks(dado)
	
		if self.salvarAtualizacaoCV:
			data = re.findall(u'Última atualização do currículo em (\d{2}/\d{2}/\d{4})', dado)
			
			if len(data) > 0: # se a data de atualizacao do CV for identificada
				#self.curriculoVitae.setDataAtualizacao
				self.atualizacaoCV = stripBlanks(data[0])
				self.registro.defineDataAtualizacaoCV(self.atualizacaoCV)
				self.salvarAtualizacaoCV = 0

		# Encontrar o titulo do cabecalho de cada secao do curriculo
		if self.procurarCabecalho:
			if u'Identificação'==dado:			#Encontrou titulo "identificacao"
				self.achouIdentificacao = 1
			if u'Endereço'==dado:
				self.achouEndereco = 1
			if u'Formação acadêmica/titulação'==dado:
				self.achouFormacaoAcademica = 1
			if u'Formação Complementar'==dado:
				self.achouFormacaoComplementar = 1
			if u'Atuação Profissional'==dado:
				self.achouAtuacaoProfissional = 1
			if u'Linhas de Pesquisa'==dado:
				self.achouLinhaPesquisa = 1
			if u'Projetos de pesquisa'==dado:
				self.achouProjetoDePesquisa = 1
			if u'Membro de corpo editorial'==dado:
				self.achouMembroDeCorpoEditorial = 1
			if u'Revisor de periódico'==dado:
				self.achouRevisorDePeriodico = 1
			if u'Áreas de atuação'==dado:
				self.achouAreaDeAtuacao = 1
			if u'Idiomas'==dado:
				self.achouIdioma = 1
			if u'Prêmios e títulos'==dado:
				self.achouPremioOuTitulo = 1

			if u'Produções'==dado:  # !---
				self.achouProducoes = 1
				self.achouProducaoEmCTA = 1
			if u'Produção técnica'==dado:
				self.achouProducaoTecnica = 1
			if u'Produção artística/cultural'==dado:
				self.achouProducaoArtisticaCultural = 1
			if u'Bancas'==dado:
				self.achouBancas = 1
			if u'Eventos'==dado:
				self.achouEventos = 1
			if u'Orientações'==dado:
				self.achouOrientacoes = 1
			if u'Outras informações relevantes'==dado:
				self.achouOutrasInformacoesRelevantes = 1
			self.umaUnidade = 0

		if self.achouIdentificacao:
			if u'Nome em citações bibliográficas'==dado:
				self.achouNomeEmCitacoes = 1
			if u'Sexo'==dado:
				self.achouSexo = 1

		if self.achouEndereco:
			if u'Endereço Profissional'==dado:
				self.achouEnderecoProfissional = 1

		#Dados gerais
		if self.achouAtuacaoProfissional:
			if u'Vínculo institucional' == dado:
				self.salvarItem = 1
				self.achouVinculoInstitucional = 1
				self.achouOutrasInformacoes = 0
				self.achouAtividades = 0
			if u'Outras informações' == dado:
				self.salvarItem = 1
				self.achouOutrasInformacoes = 1
				self.achouVinculoInstitucional = 0
				self.achouAtividades = 0
			if u'Atividades' == dado:
				self.salvarItem = 1
				self.achouAtividades = 1
				self.achouOutrasInformacoes = 0
				self.achouVinculoInstitucional = 0

		if self.achouProducoes:
			if u'Produção bibliográfica'==dado:
				self.achouProducaoEmCTA = 1
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 0
				self.achouDemaisTrabalho = 1
			if u'Produção técnica'==dado:
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 1
				self.achouProducaoArtisticaCultural= 0
				self.achouDemaisTrabalho = 0
			if u'Produção artística/cultural'==dado:
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 1
				self.achouDemaisTrabalho = 0	
			if u'Demais trabalhos'==dado:
				self.salvarItem = 0
				self.achouProducaoEmCTA = 0
				self.achouProducaoTecnica = 0
				self.achouProducaoArtisticaCultural= 0
				self.achouDemaisTrabalho = 1


			if self.achouProducaoEmCTA:
				if u'Artigos completos publicados em periódicos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 1
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Livros publicados/organizados ou edições'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 1
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Capítulos de livros publicados'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 1
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Textos em jornais de notícias/revistas'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 1
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Trabalhos completos publicados em anais de congressos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 1
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Resumos expandidos publicados em anais de congressos'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 1
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Resumos publicados em anais de congressos' in dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 1
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Artigos aceitos para publicação'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 1
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Apresentações de Trabalho'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 1
					self.achouOutroTipoDeProducaoBibliografica = 0
				if u'Outras produções bibliográficas'==dado:
				#if u'Demais tipos de produção bibliográfica'==dado:
					self.salvarItem = 1
					self.achouArtigoEmPeriodico = 0
					self.achouLivroPublicado = 0
					self.achouCapituloDeLivroPublicado = 0
					self.achouTextoEmJornalDeNoticia = 0
					self.achouTrabalhoCompletoEmCongresso = 0
					self.achouResumoExpandidoEmCongresso = 0
					self.achouResumoEmCongresso = 0
					self.achouArtigoAceito = 0
					self.achouApresentacaoDeTrabalho = 0
					self.achouOutroTipoDeProducaoBibliografica = 1

			if self.achouProducaoTecnica:
				#if u'Softwares com registro de patente'==dado:
				if u'Programas de computador com registro'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 1
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Programas de computador sem registro'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 1
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Produtos tecnológicos'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 1
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Processos ou técnicas'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 1
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Trabalhos técnicos'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 1
					self.achouOutroTipoDeProducaoTecnica = 0
				if u'Demais tipos de produção técnica'==dado:
					self.salvarItem = 1
					self.achouSoftwareComPatente = 0
					self.achouSoftwareSemPatente = 0
					self.achouProdutoTecnologico = 0
					self.achouProcessoOuTecnica = 0
					self.achouTrabalhoTecnico = 0
					self.achouOutroTipoDeProducaoTecnica = 1
				#if u'Demais trabalhos'==dado:
				#	self.salvarItem = 0
				#	self.achouSoftwareComPatente = 0
				#	self.achouSoftwareSemPatente = 0
				#	self.achouProdutoTecnologico = 0
				#	self.achouProcessoOuTecnica = 0
				#	self.achouTrabalhoTecnico = 0
				#	self.achouOutroTipoDeProducaoTecnica = 0
    
			if self.achouProducaoArtisticaCultural:
				#if u'Produção artística/cultural'==dado:
				if u'Outras produções artísticas/culturais'==dado:
					self.salvarItem = 1
					self.achouOutraProducaoArtisticaCultural = 1
					self.achoArtesCenicas = 0
					self.achouMusica = 0
				if u'Artes Cênicas'==dado:
					self.salvarItem = 1
					self.achouOutraProducaoArtisticaCultural = 0
					self.achoArtesCenicas = 1
					self.achouMusica = 0
				if u'Música'==dado:
					self.salvarItem = 1
					self.achouOutraProducaoArtisticaCultural = 0
					self.achoArtesCenicas = 0
					self.achouMusica = 1
		
		if self.achouBancas:
			if u'Participação em bancas de trabalhos de conclusão'==dado:
				self.achouBancaTC = 1
				self.achouBancaCJ = 0
			if u'Participação em bancas de comissões julgadoras'==dado:			
				self.achouBancaCJ = 1
				self.achouBancaTC = 0
			if self.achouBancaTC:
				if u'Qualificações de Doutorado'==dado:
					self.salvarItem = 1
					self.achouBancaMestrado = 0
					self.achouBancaTCC = 0
					self.achouBancaQualificacaoDoutorado = 1
					self.achouBancaQualificacaoMestrado = 0
				if u'Qualificações de Mestrado'==dado:
					self.salvarItem = 1
					self.achouBancaMestrado = 0
					self.achouBancaTCC = 0
					self.achouBancaQualificacaoDoutorado = 0
					self.achouBancaQualificacaoMestrado = 1
				if u'Monografias de cursos de aperfeiçoamento/especialização'==dado:
					self.salvarItem = 1
					self.achouBancaMestrado = 0
					self.achouBancaTCC = 0
					self.achouBancaQualificacaoDoutorado = 0
					self.achouBancaQualificacaoMestrado = 0
					self.achouBancaAperfeicoamentoEspecializacao = 1
				if u'Mestrado'==dado:
					self.salvarItem = 1
					self.achouBancaMestrado = 1
					self.achouBancaTCC = 0
					self.achouBancaQualificacaoDoutorado = 0
					self.achouBancaQualificacaoMestrado = 0
					self.achouBancaAperfeicoamentoEspecializacao = 0
				if u'Trabalhos de conclusão de curso de graduação'==dado:
					self.salvarItem = 1
					self.achouBancaTCC = 1
					self.achouBancaMestrado = 0
					self.achouBancaQualificacaoDoutorado = 0
					self.achouBancaQualificacaoMestrado = 0
					self.achouBancaAperfeicoamentoEspecializacao = 0
			if self.achouBancaCJ:
				if u'Concurso público'==dado:
					self.salvaItem = 1
					self.achouBancaCP = 1
					self.achouBancaOP = 0
					self.achouBancaAC = 0
				if u'Outras participações'==dado:
					self.salvarItem = 1
					self.achouBancaOP = 1
					self.achouBancaCP = 0
					self.achouBancaAC = 0
				if u'Avaliação de cursos'==dado:
					self.salvarItem = 1
					self.achouBancaOP = 0
					self.achouBancaCP = 0
					self.achouBancaAC = 1

		if self.achouEventos:
			if u'Participação em eventos, congressos, exposições e feiras'==dado:
				self.salvarItem = 1
				self.achouParticipacaoEmEvento  = 1
				self.achouOrganizacaoDeEvento = 0
			if u'Organização de eventos, congressos, exposições e feiras'==dado:
				self.salvarItem = 1
				self.achouParticipacaoEmEvento  = 0
				self.achouOrganizacaoDeEvento = 1

		if self.achouOrientacoes:
			if u'Orientações e supervisões em andamento'==dado:
				self.achouOrientacoesEmAndamento  = 1
				self.achouOrientacoesConcluidas = 0
			if u'Orientações e supervisões concluídas'==dado:
				self.achouOrientacoesEmAndamento  = 0
				self.achouOrientacoesConcluidas = 1

			# Tipos de orientações (em andamento ou concluídas)
			if u'Supervisão de pós-doutorado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 1
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Tese de doutorado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 1
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Dissertação de mestrado'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 1
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Monografia de conclusão de curso de aperfeiçoamento/especialização'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 1
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Trabalho de conclusão de curso de graduação'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 1
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 0
			if u'Iniciação científica' in dado or u'Iniciação Científica'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 1
				self.achouOutroTipoDeOrientacao = 0
			if u'Orientações de outra natureza'==dado:
				self.salvarItem = 1
				self.achouSupervisaoDePosDoutorado = 0
				self.achouTeseDeDoutorado = 0
				self.achouDissertacaoDeMestrado = 0
				self.achouMonografiaDeEspecializacao = 0
				self.achouTCC = 0
				self.achouIniciacaoCientifica = 0
				self.achouOutroTipoDeOrientacao = 1


		if self.achouOutrasInformacoesRelevantes:
			self.salvarItem = 1
				
		if self.recuperarIdentificador16 and self.identificador16 == '':
		  id = re.findall(u'http://lattes.cnpq.br/(\d{16})', dado)
		  if len(id) > 0:
		    self.identificador16 = id[0]

		if self.achouProjetoDePesquisa:
			if u'Projeto certificado pelo(a) coordenador(a)' in dado or u'Projeto certificado pela empresa' in dado:
				self.item = ''
				self.salvarParte3 = 0



# ---------------------------------------------------------------------------- #
def stripBlanks(s):
	return re.sub('\s+', ' ', s).strip()

def htmlentitydecode(s):                                                                               
	return re.sub('&(%s);' % '|'.join(name2codepoint),                                                 
		lambda m: unichr(name2codepoint[m.group(1)]), s)   

