#!/usr/bin/python
# encoding: utf-8
# filename: apresentacaoDeTrabalho.py
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

class ApresentacaoDeTrabalho(ProducaoBibliografica):
	
	natureza = '' # tipo de apresentacao

	def __init__(self, idMembro, tipo, partesDoItem=''):
		ProducaoBibliografica.__init__(self, tipo, idMembro)
		if not partesDoItem=='': 
			# partesDoItem[0]: Numero (NAO USADO)
			# partesDoItem[1]: Descricao do livro (DADO BRUTO)
			self.item = partesDoItem[1]

			# Dividir o item na suas partes constituintes
			partes = self.item.partition(" . ")		#Separa o nome dos autores
			self.autores = partes[0].strip()		#Retira o espaco da string nome dos autores
			partes = partes[2]				#Titulo do do tra

			aux = re.findall(u' \((.*?)\)', partes)
			if len(aux)>0:
				aux = aux[-1]
				partes = partes.rpartition(" (")
				partes = partes[0]
				if not aux.find('/') == -1:
					aux = aux.partition('/')
					if aux[1] != '':
						self.natureza = aux[2]
			else:
				self.natureza = ''
	
			aux = re.findall(u'. ((?:19|20)\d\d)\\b', partes)
			if len(aux)>0:
				self.ano = aux[-1] #.strip().rstrip(".").rstrip(",")
				partes = partes.rpartition(". ")
				partes = partes[0]
			else:
				self.ano = ''
	
			self.titulo = partes.strip().rstrip(".")
			self.chave = self.autores # chave de comparação entre os objetos

		else:
			self.autores = ''
			self.titulo = ''
			self.ano = ''
			self.natureza = ''

	# ------------------------------------------------------------------------ #
	def __str__(self):
		s  = "\n[APRESENTACAO DE TRABALHO] \n"
		s += "+ID-MEMBRO   : " + str(self.idMembro) + "\n"
		s += "+RELEVANTE   : " + str(self.relevante) + "\n"
		s += "+AUTORES     : " + self.autores.encode('utf8','replace') + "\n"
		s += "+TITULO      : " + self.titulo.encode('utf8','replace') + "\n"
		s += "+ANO         : " + str(self.ano) + "\n"
		s += "+NATUREZA    : " + self.natureza.encode('utf8','replace') + "\n"
		s += "+item        : " + self.item.encode('utf8','replace') + "\n"
		return s
