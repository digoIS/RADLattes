#!/usr/bin/python
# encoding: utf-8

import fileinput
import sets
import operator

from parserLattes  	    import *
from interfaceComunicacao   import *
from gerenciadorComunicacao import *
from gerenciadorRegistro    import *
from pesquisador 	    import *

#ControladorExtracao: - arquivo de configuracao [arquivo de banco de dados] e id do curriculo.
class ControladorExtracao:

	
	#arquivoConfigBanco  = None
	itemsDesdeOAno    = None
	itemsAteOAno      = None
	diretorioCache    = None
	listaDeParametros = []
	gerenciadorComunicacao = None
	
	# Defini o periodo da busca e cria um diretoria para cache
	def __init__(self, arquivo):
		
		self.carregarParametrosPadrao()
		self.carregarParametrosPersonalizados(arquivo)
		
		# carregamos o periodo global
		ano1 = self.obterParametro('global-itens_desde_o_ano')
		ano2 = self.obterParametro('global-itens_ate_o_ano')

		if ano1.lower() == 'hoje':
			ano1 = str(datetime.datetime.now().year)
		if ano2.lower() == 'hoje':
			ano2 = str(datetime.datetime.now().year)
		if ano1 == '':
			ano1 = '0'
		if ano2 == '':
			ano2 = '10000'

		self.itemsDesdeOAno = int(ano1)
		self.itemsAteOAno   = int(ano2)

		self.diretorioCache = self.obterParametro('global-diretorio_de_armazenamento_de_cvs')
		if not self.diretorioCache == '':
			criarDiretorio(self.diretorioCache)

		
		self.gerenciadorComunicacao = GerenciadorComunicacao(self.itemsDesdeOAno, self.itemsAteOAno, self.diretorioCache)
		self.carregarPesquisadores()
				
	def importarRelatorioAtividadeDocente(self):
		self.gerenciadorComunicacao.descarregarCurriculos()	#Baixa os curriculos da plataforma Lattes
		lista = self.gerenciadorComunicacao.listaPesquisador	#Obter a lista de pesquisadores do gerenciador de comunicacao
		for pesquisador in lista:
			parser      = ParserLattes(pesquisador.idMembro, pesquisador.curriculoHTML)
			
			registro    = parser.obterRegistroAtividades()	
			print 'Nome Completo', registro.nomeCompleto

			gerenciadorRegistro    = GerenciadorRegistro()			
			gerenciadorRegistro.inserirRegistro(registro)	#Insere os dados do pesquisador na base de dados.
			gerenciadorRegistro = None


	def carregarParametrosPersonalizados(self, arquivo):
		# Atualizamos a lista de parametros a partir do arquivo de configuracao
		for linha in fileinput.input(arquivo):
			linha = linha.replace("\r","")
			linha = linha.replace("\n","")
			
			linhaPart = linha.partition("#") 		#eliminamos os comentários
			linhaDiv  = linhaPart[0].split("=",1)

			if len(linhaDiv) == 2:
				self.atualizarParametro(linhaDiv[0], linhaDiv[1])

	def carregarPesquisadores(self):	
		idSequencial = 1
		#Abertura do arquivo com os identificadores de cada docente
		for linha in fileinput.input(self.obterParametro('global-arquivo_de_entrada')):
			linha = linha.replace("\r","") 						#Substitui retorno por vazio	
			linha = linha.replace("\n","")						#Substitui quebra de linha por vazio	
			
			linhaPart = linha.partition("#") 					# elimina os comentários
			linhaDiv  = linhaPart[0].split(",") 

			if not linhaDiv[0].strip() == '':
				identificador = linhaDiv[0].strip() if len(linhaDiv)>0  else ''
				nome          = linhaDiv[1].strip() if len(linhaDiv)>1  else ''
				periodo       = linhaDiv[2].strip() if len(linhaDiv)>2  else ''
				pesquisador = Pesquisador(idSequencial, identificador, nome, periodo)
				print 'URL', pesquisador.url
				self.gerenciadorComunicacao.listaPesquisador.append(pesquisador)
				idSequencial = idSequencial + 1

		
				
	def atualizarParametro(self, parametro, valor):
		parametro = parametro.strip().lower()
		valor = valor.strip()

		for i in range(0,len(self.listaDeParametros)):
			if parametro==self.listaDeParametros[i][0]:		
				self.listaDeParametros[i][1] = valor
				return
		print "[AVISO IMPORTANTE] Nome de parametro desconhecido: "+parametro
	
	def obterParametro(self, parametro):
		for i in range(0,len(self.listaDeParametros)):
			if parametro == self.listaDeParametros[i][0]:
				if self.listaDeParametros[i][1].lower()=='sim':
					return 1
				if self.listaDeParametros[i][1].lower()=='nao' or self.listaDeParametros[i][1].lower()=='não':
					return 0
				
				return self.listaDeParametros[i][1]

	# Cria uma lista com parametros default: podera ser definido pelo usuario.
	def carregarParametrosPadrao(self):
		self.listaDeParametros.append(['global-nome_do_grupo', ''])
		self.listaDeParametros.append(['global-arquivo_de_entrada', ''])
		self.listaDeParametros.append(['global-diretorio_de_saida', ''])
		self.listaDeParametros.append(['global-email_do_admin', ''])
		self.listaDeParametros.append(['global-idioma', 'PT'])
		self.listaDeParametros.append(['global-itens_desde_o_ano', '']) 
		self.listaDeParametros.append(['global-itens_ate_o_ano', ''])      # hoje
		self.listaDeParametros.append(['global-itens_por_pagina', '1000'])
		self.listaDeParametros.append(['global-criar_paginas_jsp', 'nao'])
		self.listaDeParametros.append(['global-google_analytics_key', ''])
		self.listaDeParametros.append(['global-prefixo', ''])
		self.listaDeParametros.append(['global-diretorio_de_armazenamento_de_cvs', ''])
		self.listaDeParametros.append(['global-diretorio_de_armazenamento_de_doi', ''])
		self.listaDeParametros.append(['global-salvar_informacoes_em_formato_xml', 'nao'])

		self.listaDeParametros.append(['global-identificar_publicacoes_com_qualis', 'nao'])
		self.listaDeParametros.append(['global-arquivo_qualis_de_periodicos', ''])
		self.listaDeParametros.append(['global-arquivo_qualis_de_congressos', ''])

		self.listaDeParametros.append(['relatorio-salvar_publicacoes_em_formato_ris', 'nao'])
		self.listaDeParametros.append(['relatorio-incluir_artigo_em_periodico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_livro_publicado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_capitulo_de_livro_publicado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_texto_em_jornal_de_noticia', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_trabalho_completo_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_resumo_expandido_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_resumo_em_congresso', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_artigo_aceito_para_publicacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_apresentacao_de_trabalho', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_outro_tipo_de_producao_bibliografica', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_software_com_patente', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_software_sem_patente', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_produto_tecnologico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_processo_ou_tecnica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_trabalho_tecnico', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_outro_tipo_de_producao_tecnica', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_producao_artistica', 'sim'])

		self.listaDeParametros.append(['relatorio-mostrar_orientacoes', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_mestrado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_monografia_de_especializacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_tcc', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_iniciacao_cientifica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_em_andamento_outro_tipo', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_doutorado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_mestrado', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_monografia_de_especializacao', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_tcc', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_iniciacao_cientifica', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_orientacao_concluida_outro_tipo', 'sim'])

		self.listaDeParametros.append(['relatorio-incluir_projeto', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_premio', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_participacao_em_evento', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_organizacao_de_evento', 'sim'])
		self.listaDeParametros.append(['relatorio-incluir_internacionalizacao', 'nao'])

		self.listaDeParametros.append(['grafo-mostrar_grafo_de_colaboracoes', 'sim'])
		self.listaDeParametros.append(['grafo-mostrar_todos_os_nos_do_grafo', 'sim'])
		self.listaDeParametros.append(['grafo-considerar_rotulos_dos_membros_do_grupo', 'sim'])
		self.listaDeParametros.append(['grafo-mostrar_aresta_proporcional_ao_numero_de_colaboracoes', 'sim'])
		
		self.listaDeParametros.append(['grafo-incluir_artigo_em_periodico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_livro_publicado', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_capitulo_de_livro_publicado', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_texto_em_jornal_de_noticia', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_trabalho_completo_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_resumo_expandido_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_resumo_em_congresso', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_artigo_aceito_para_publicacao', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_apresentacao_de_trabalho', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_outro_tipo_de_producao_bibliografica', 'sim'])

		self.listaDeParametros.append(['grafo-incluir_software_com_patente', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_software_sem_patente', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_produto_tecnologico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_processo_ou_tecnica', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_trabalho_tecnico', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_outro_tipo_de_producao_tecnica', 'sim'])

		self.listaDeParametros.append(['grafo-incluir_producao_artistica', 'sim'])
		self.listaDeParametros.append(['grafo-incluir_grau_de_colaboracao', 'nao'])

		self.listaDeParametros.append(['mapa-mostrar_mapa_de_geolocalizacao', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_membros_do_grupo', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_pos_doutorado', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_doutorado', 'sim'])
		self.listaDeParametros.append(['mapa-incluir_alunos_de_mestrado', 'nao'])

