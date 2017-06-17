#!/usr/bin/python
# encoding: utf-8
# filename: capituloDeLivroPublicado.py
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

class CapituloDeLivroPublicado(ProducaoBibliografica):
	
	livro = None
	editora = None
	edicao = None
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

			partes = partes.rpartition(" p.")
			if partes[1]=='': # se nao existem paginas
				self.paginas = ''
				partes = partes[2]
			else:
				self.paginas = partes[2].strip().rstrip(".").rstrip("-").strip()
				partes = partes[0]

			partes = partes.rpartition(" v. ")
			if partes[1]=='': # se nao existem informacao de volume
				self.volume = ''
				partes = partes[2]
			else:
				self.volume = partes[2].rstrip(".").rstrip(",")
				partes = partes[0]

			partes = partes.rpartition(", ")
			self.ano = partes[2].strip().rstrip(".").rstrip(",")
			partes = partes[0]

			partes = partes.rpartition(". ed. ")
			if partes[1]=='': # se nao existe edicao
				self.edicao = ''
				partes = partes[2]
			else:
				partes = partes[0].rpartition(" ")
				self.edicao = partes[2]
				partes = partes[0]

			partes = partes.rpartition(": ")
			if partes[1]=='': # se nao existe editora 
				self.editora = ''
				partes = partes[2]
			else:
				self.editora = partes[2].strip()
				partes = partes[0]

			partes = partes.partition(" In: ")
			if partes[1] == '': # se nao existe titulo de livro 
				try:
					p = partes[0].rpartition(".")
					self.titulo = p[0].partition(".")[0]
					self.local = p[2]
				except:
					print ('Capitulo de livro - Falha ao inserir titulo e local.')
					print "TITULO", self.titulo
					print "LOCAL ", self.local 
			else:
				self.titulo = partes[0].partition(".")[0]
				self.local = ""
				'''if plivro[1] == '':
					self.livro = partes[2].strip().rstrip(".")
				else:
					self.livro = plivro[2].partition('.')[0].strip()
					self.local = plivro[2].rpartition(".")[2].strip()
					if self.local[1] == '' or len(self.local) > 20 or self.local.find('ed') != -1:
						self.local = ''
					else:
						l = ['/', '-', ',']
						for i in l:
							p = self.local.partition(i)
							if p[1] != '':
								self.local = p[0].strip()
						if self.local.find('RS') != -1:
							self.local = self.local.partition(" ")[0].strip()		
				partes = partes[0]'''
			self.livro = ""	
			if self.volume == None:
				 self.volume = ''	
		else:
			self.autores = ''
			self.titulo = ''
			self.livro = ''
			self.edicao = ''
			self.editora = ''
			self.ano = ''
			self.volume = ''
			self.paginas = ''
			self.chave = ''


	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[CAPITULO DE LIVRO PUBLICADO] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+RELEVANTE   : " + str(self.relevante) + "\n"
		s += "+AUTORES     : " + self.autores.encode('utf8','replace') + "\n"
		s += "+TITULO      : " + self.titulo.encode('utf8','replace') + "\n"
		s += "+LIVRO       : " + self.livro.encode('utf8','replace') + "\n"
		s += "+EDICAO      : " + self.edicao.encode('utf8','replace') + "\n"
		s += "+EDITORA     : " + self.editora.encode('utf8','replace') + "\n"
		s += "+ANO         : " + str(self.ano) + "\n"
		s += "+VOLUME      : " + self.volume.encode('utf8','replace') + "\n"
		s += "+PAGINAS     : " + self.paginas.encode('utf8','replace') + "\n"
		s += "+item        : " + self.item.encode('utf8','replace') + "\n"
		return s
