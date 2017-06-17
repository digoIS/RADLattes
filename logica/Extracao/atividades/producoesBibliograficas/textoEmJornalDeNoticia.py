#!/usr/bin/python
# encoding: utf-8
# filename: textoEmJornalDeNoticia.py
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

class TextoEmJornalDeNoticia(ProducaoBibliografica):

	nomeJornal = None
	data = None	
	local = None
	
	def __init__(self, idMembro, tipo, partesDoItem=''):
		ProducaoBibliografica.__init__(self, tipo, idMembro)
		if not partesDoItem=='': 
			# partesDoItem[0]: Numero (NAO USADO)
			# partesDoItem[1]: Descricao do livro (DADO BRUTO)
			self.item = partesDoItem[1]
			
			# Dividir o item na suas partes constituintes
			partes = self.item.partition(" . ")
			self.autores = partes[0].strip()
			partes = partes[2]

			if len(re.findall(u'\d\d \w+. (?:19|20)\d\d', partes))>0:
				partes = partes.rpartition(",")
				self.data = partes[2].strip().rstrip(".").rstrip(",")
				partes = partes[0]
			else:
				self.data = ''

			aux = re.findall(' ((?:19|20)\d\d)\\b', self.data)
			if len(aux)>0:
				self.ano = aux[-1]
			else:
				self.ano = ''

			partes = partes.rpartition(" p. ")
			if partes[1]=='': # se nao existem paginas
				self.paginas = ''
				partes = partes[2]
			else:
				self.paginas = re.sub(r'\s', '', partes[2]).rstrip(".").rstrip(",")
				partes = partes[0]
		
			partes = partes.rpartition(" v. ")
			if partes[1]=='': # se nao existem informacao de volume
				self.volume = ''
				partes = partes[2]
			else:
				self.volume = partes[2].rstrip(".").rstrip(",")
				partes = partes[0]

			partes = partes.rpartition(". ")
			pjornal = partes[2].strip().rstrip('.').rstrip(",")
			flag = False
			if not pjornal.find(')') == -1:
				pjornal = pjornal.partition("),")
				flag = True 		
			else:
				pjornal = pjornal.partition(", ")
			
			if pjornal[1] == '':
				self.nomeJornal = partes[2].strip().rstrip('.').rstrip(",")
				self.local = ''
			else:
				self.nomeJornal = pjornal[0].strip().rstrip(".")
				if flag:
					self.nomeJornal = pjornal[0].partition("(")[0].strip()
				self.local = pjornal[2].partition(',')[0].strip()
				
			partes = partes[0]
			self.titulo = partes.strip().rstrip(".")

			if self.volume == None:
				 self.volume = ''
		else:
			self.autores = ''
			self.titulo = ''
			self.nomeJornal = ''
			self.data = ''
			self.volume = ''
			self.paginas = ''
			self.ano = ''


	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[TEXTO EM JORNAL DE NOTICIA/REVISTA] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+RELEVANTE   : " + str(self.relevante) + "\n"
		s += "+AUTORES     : " + self.autores.encode('utf8','replace') + "\n"
		s += "+TITULO      : " + self.titulo.encode('utf8','replace') + "\n"
		s += "+NOME MEDIO  : " + self.nomeJornal.encode('utf8','replace') + "\n"
		s += "+DATA        : " + self.data.encode('utf8','replace') + "\n"
		s += "+ANO (oculto): " + str(self.ano) + "\n"
		s += "+VOLUME      : " + self.volume.encode('utf8','replace') + "\n"
		s += "+PAGINAS     : " + self.paginas.encode('utf8','replace') + "\n"
		s += "+item        : " + self.item.encode('utf8','replace') + "\n"
		return s
