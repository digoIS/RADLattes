#!/usr/bin/python
# encoding: utf-8
# filename: resumoEmCongresso.py
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

from producaoBibliografica import *
#from scriptLattes import *
import re

class ResumoEmCongresso(ProducaoBibliografica):
	
	nomeDoEvento   = None
	anoEvento      = None
	localDoEvento  = None
	tituloDosAnais = None
	numero         = None

	def __init__(self, idMembro, tipo, partesDoItem='', doi=''):
		ProducaoBibliografica.__init__(self, tipo, idMembro)
		if not partesDoItem=='': 
			# partesDoItem[0]: Numero (NAO USADO)
			# partesDoItem[1]: Descricao do artigo (DADO BRUTO)
			self.item = partesDoItem[1]
			self.doi = doi
			# Dividir o item na suas partes constituintes
			partes = self.item.partition(" . ")
			self.autores = partes[0].strip()
			partes = partes[2]

			#-------------------------
			aux = re.findall(u', ((?:19|20)\d\d)\\b', partes)
			if len(aux)>0:
	#			partes = partes.rpartition(",")
				self.ano = aux[-1].strip().rstrip(".").rstrip(",")
	#			partes = partes[0]
			else:
				self.ano = ''					#Casa com a ultima instancia de ano na string
			#------------------------

			partes = partes.rpartition(" p. ")
			if partes[1]=='': # se nao existem paginas
				self.paginas = ''
				partes = partes[2]
			else:
				self.paginas = partes[2].rstrip(".")
				partes = partes[0]

			partes = partes.rpartition(", n. ")
			if partes[1]=='': # se nao existe numero
				self.numero = ''
				partes = partes[2]
			else:
				self.numero = partes[2].strip().rstrip(",")
				partes = partes[0]
			
			partes = partes.rpartition(" v. ")
			if partes[1]=='': # se nao existem informacao de volume
				self.volume = ''
				partes = partes[2]
			else:
				self.volume = partes[2].rstrip(".").rstrip(",")
				partes = partes[0]
	
			aux = re.findall(u', ((?:19|20)\d\d)\\b', partes)
			if len(aux) > 0:
				partes = partes.rpartition(",")
				self.ano = aux[-1].strip().rstrip(".").rstrip(",")
				partes = partes[0]
			else:
				self.ano = ''

			#self.titulo = partes.strip().rstrip(".").rstrip(",")
			self.chave = self.autores 				# chave de comparação entre os objetos
			pattern = re.compile(r'(\d{4},\s\w+(\s*\w)*)')
			result = re.findall(pattern, partes)
			if len(result) > 0:
				pattern = result
			else:
				pattern = ['']

			#Cursos de curta duracao
			if not partes.find(" In: ") == -1:
				partes = partes.partition(" In: ")#strip().rstrip(".").rstrip(",")
				if not partes[1] == '':
					self.titulo = partes[0]
					self.nomeDoEvento = partes[2].partition(",")[0].strip()
				else:
					self.titulo = partes[0]
					self.nomeDoEvento = ""

			if self.nomeDoEvento == None:
				self.nomeDoEvento = ''
			if self.titulo == None:
				self.titulo = ''

			if not pattern[0] == '':
				self.localDoEvento = str(pattern[0][0].partition(',')[2].strip())
			elif self.localDoEvento == None:
				self.localDoEvento = ''

			if self.volume == None:
				 self.volume = ''

		else:
			self.doi = ''
			self.autores = ''
			self.titulo = ''
			self.nomeDoEvento = ''
			self.ano = ''
			self.volume = ''
			self.numero = ''
			self.paginas = ''

	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[RESUMO EM CONGRESSO] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+RELEVANTE   : " + str(self.relevante) + "\n"
		s += "+DOI         : " + self.doi.encode('utf8','replace') + "\n"
		s += "+AUTORES     : " + self.autores.encode('utf8','replace') + "\n"
		s += "+TITULO      : " + self.titulo.encode('utf8','replace') + "\n"
		s += "+NOME EVENTO : " + self.nomeDoEvento.encode('utf8','replace') + "\n"
		s += "+ANAIS       : " + self.tituloDosAnais.encode('utf8','replace') + "\n"
		s += "+ANO         : " + str(self.ano) + "\n"
		s += "+VOLUME      : " + self.volume.encode('utf8','replace') + "\n"
		s += "+NUMERO      : " + self.numero.encode('utf8','replace') + "\n"
		s += "+PAGINAS     : " + self.paginas.encode('utf8','replace') + "\n"
		s += "+item        : " + self.item.encode('utf8','replace') + "\n"

		return s
