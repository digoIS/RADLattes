#!/usr/bin/python
# encoding: utf-8
# filename: projetoDePesquisa.py
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

#from geradorDePaginasWeb import *
from string import *
import datetime
import re

class ProjetoDePesquisa:
	idMembro = None
	anoInicio = None
	anoConclusao = None
	nome = ''
	descricao = ''
	ano = None
	################## ELEMENTOS DA DESCRICAO DO PROJETO ################
	situacao = ''
	natureza = ''
	coordenador = ''
	atividade = ''
	integrantes = None
	financiadores = None

	######################################################################
	def __init__(self, idMembro, partesDoItem):
		# partesDoItem[0]: Periodo do projeto de pesquisa
		# partesDoItem[1]: cargo e titulo do projeto
		# partesDoItem[2]: Descricao (resto)

		self.financiadores = []
		self.integrantes = []

		anos =  partesDoItem[0].partition(" - ")
		self.anoInicio = anos[0]
		self.anoConclusao = anos[2]
	
		self.nome = partesDoItem[1]
		self.descricao = list([])
		
		patterDescricao      = "Descrição:".decode('utf8')
		patternSituacao      = "Situação:".decode('utf8')		
		patternIntegrante    = "Integrantes:".decode('utf8')
		patternFinanciadores = "Financiador(es):".decode('utf8')
		patternNumProducoes  = "Número de produções".decode('utf8')
		
		s = ''

		if not partesDoItem[2].find(patterDescricao) == -1:
			partes = partes = partesDoItem[2].partition(patterDescricao)
			self.descricao.append(partes[2].partition(patternSituacao)[0].strip().rstrip("."))
		else:
			self.descricao.append('')
			s += ' + NAO HA DESCRICAO DO PROJETO \n'

		if not partesDoItem[2].find(patternSituacao) == -1:
			partes = partesDoItem[2].partition(patternSituacao)
			partes = partes[2].partition(patternIntegrante)
			self.situacao = partes[0].partition(";")[0].strip()
			self.natureza = partes[0].partition(":")[2].partition(".")[0].strip()
		else:
			s += ' + NAO HA SITUACAO CADASTRADA \n'
				

		if not partesDoItem[2].find(patternIntegrante) == -1:
			partes = partesDoItem[2].partition(patternIntegrante)
			partes = partes[2].partition(patternFinanciadores)
			integrantes = partes[0].rpartition(".")[0].strip()
			itens = integrantes.split(" / ")
			for item in itens:
				 try:
					(nome, participacao) = item.split(" - ")
					self.integrantes.append((nome.strip(), participacao.strip().rstrip(".")))
				 except:
					print ('Ocorre uma falha com os membros do projeto!')
					print "LISTA DE MEMBROS - ", self.integrantes
			
		else:
			s += ' + NAO HA INTEGRANTES \n'
			
		if not partesDoItem[2].find(patternFinanciadores) == -1:
			partes = partesDoItem[2].partition(patternFinanciadores)
			partes = partes[2].partition(patternNumProducoes)[0].rstrip(".")
			itens = partes.split("/")
			for item in itens:
				try:
					(nome, bolsa) = item.split(" - ")
					self.financiadores.append((nome, bolsa))
				except:
					print ('Ocorre uma falha com os financiadores!')
					print "LISTA DE FINANCIADORES - ", self.financiadores
		else:	
			s += ' + NAO HA FINANCIADORES CADASTRADOS \n'
		
		if not s == '':
			print s 
											
	def __str__(self):
		s  = "\n[PROJETO DE PESQUISA] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+ANO INICIO  : " + str(self.anoInicio) + "\n"
		s += "+ANO CONCLUS.: " + str(self.anoConclusao) + "\n"
		s += "+NOME        : " + self.nome.encode('utf8','replace') + "\n"
		s += "+DESCRICAO   : " + str(self.descricao).encode('utf8','replace') + "\n"
		return s

