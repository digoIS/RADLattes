#!/usr/bin/python
# encoding: utf-8
# filename: livroPublicado.py
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

class LivroPublicado(ProducaoBibliografica):

	edicao = None
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
			partes = partes.rpartition("p .")
			
			if partes[1]=='': # se nao existem paginas
				self.paginas = ''
				partes = partes[2]
				#print partes
			else:
				partes = partes[0].rpartition(". ")
				self.paginas = partes[2]
				partes = partes[0]
		
			partes = partes.rpartition(" v. ")
			if partes[1]=='': # se nao existem informacao de volume
				self.volume = ''
				partes = partes[2]
			else:
				self.volume = partes[2].rstrip(".")
				partes = partes[0]
	
			partes = partes.rpartition(", ")
			self.ano = partes[2].strip().rstrip(".")
			partes = partes[0]

			partes = partes.rpartition(". ed. ")
			if partes[1]=='': # se nao existe edicao
				self.edicao = ''
				partes = partes[2]
			else:
				partes = partes[0].rpartition(" ")
				self.edicao = partes[2]
				partes = partes[0]

			self.titulo = partes.strip().rstrip(".")

			if self.volume == None:
				 self.volume = ''

		else:
			autores = ''
			titulo = ''
			edicao = ''
			ano = ''
			volume = ''
			paginas = ''



	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[LIVRO PUBLICADO] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+RELEVANTE   : " + str(self.relevante) + "\n"
		s += "+AUTORES     : " + self.autores.encode('utf8','replace') + "\n"
		s += "+TITULO      : " + self.titulo.encode('utf8','replace') + "\n"
		s += "+EDICAO      : " + self.edicao.encode('utf8','replace') + "\n"
		s += "+ANO         : " + str(self.ano) + "\n"
		s += "+VOLUME      : " + self.volume.encode('utf8','replace') + "\n"
		s += "+PAGINAS     : " + self.paginas.encode('utf8','replace') + "\n"
		s += "+item        : " + self.item.encode('utf8','replace') + "\n"
		return s
