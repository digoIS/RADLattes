#!/usr/bin/python
# encoding: utf-8
# filename: orientacaoEmAndamento.py
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


#from scriptLattes import *  
#from geradorDePaginasWeb import *
import re
class OrientacaoEmAndamento:
	item = None # dado bruto
	idMembro = []
	idOrientando = ''

	nome = None
	tituloDoTrabalho = None
	ano = None # ano de inicio
	instituicao = None
	curso = None
	agenciaDeFomento = None
	tipoDeOrientacao = None
	tipoTrabalho = None
	chave = None

	def __init__(self, idMembro, partesDoItem, idOrientando):
		# partesDoItem[0]: Numero (NAO USADO)
		# partesDoItem[1]: Descricao
		self.idMembro = set([])
		self.idMembro.add(idMembro)
		
		self.item = partesDoItem[1]
		self.idOrientando = str(idOrientando)

		# Dividir o item na suas partes constituintes 
		partes = self.item.partition(". (Orientador).")
		if not partes[1]=='': 
			self.tipoDeOrientacao = 'Orientador'
			partes = partes[0]
		else:
			partes = self.item.partition(". (Co-orientador).")
			if not partes[1]=='':
				self.tipoDeOrientacao = 'Co-orientador'
				partes = partes[0]
			else:
				self.tipoDeOrientacao = 'Supervisor'
				partes = partes[0]
		
		partes1 = partes.partition(u'. Início: ')
		partes = partes1[0].rpartition(". ")
		if not partes[1]=='':
			self.nome = partes[0].strip(".").strip(",")
			self.tituloDoTrabalho = partes[2]
		else:
			self.nome = partes[2].strip(".").strip(",")
			self.tituloDoTrabalho = ''

		partes =  partes1[2].partition(". ")	
		self.ano = partes[0]
		partes = partes[2]

		aux = re.findall(u'((?:19|20)\d\d)\\b', self.ano)
		if len(aux)>0:
			self.ano = aux[0] #.strip().rstrip(".").rstrip(",")
		else:
			self.ano = ''

		partes = partes.rpartition(", ")
		if not partes[1]=='':
			p = partes[0]
			self.agenciaDeFomento = partes[2]
		else:
			p = partes[2]
			self.agenciaDeFomento = ''

		partes = p.partition("-")
		if partes[1] == '':
			self.instituicao = p
		else:
			self.instituicao = partes[2].strip()
			partes = partes[0].rpartition("(")
			if partes[1] == "":
				self.tipoTrabalho = partes[0]
			else:
				self.curso = partes[2].split(")")[0].split(" em ")[1].strip()
				self.tipoTrabalho  = partes[0].strip()

		if self.curso == None:
			self.curso = ''		
		if self.tipoTrabalho == None:
			self.tipoTrabalho = ''
		
	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[ORIENTANDO] \n"
		s += "+ID-ORIENTADOR: " + str(self.idMembro) + "\n"
		s += "+ID-ALUNO     : " + self.idOrientando.encode('utf8','replace') + "\n"
		s += "+NOME         : " + self.nome.encode('utf8','replace') + "\n"
		s += "+TITULO TRAB. : " + self.tituloDoTrabalho.encode('utf8','replace') + "\n"
		s += "+ANO INICIO   : " + str(self.ano) + "\n"
		s += "+INSTITUICAO  : " + self.instituicao.encode('utf8','replace') + "\n"
		s += "+AGENCIA      : " + self.agenciaDeFomento.encode('utf8','replace') + "\n"
		s += "+TIPO ORIENTA.: " + self.tipoDeOrientacao.encode('utf8','replace') + "\n"
		s += "+CURSO       .: " + self.curso.encode('utf8','replace') + "\n"
		s += "+TIPO TRABALH.: " + self.tipoTrabalho.encode('utf8','replace') + "\n"
#		s += "+item         : @@" + self.item.encode('utf8','replace') + "@@\n"

		return s
