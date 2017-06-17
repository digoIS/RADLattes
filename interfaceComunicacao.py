#!/usr/bin/python

import sys
import os

sys.path.append('apresentacao/')
sys.path.append('logica/')
sys.path.append('logica/Extracao')
sys.path.append('logica/Extracao/atividades/producoesBibliograficas/')
sys.path.append('logica/Extracao/atividades/producoesTecnicas/')
sys.path.append('logica/Extracao/atividades/producoesArtisticas/')
sys.path.append('logica/Extracao/atividades/producoesUnitarias/')
sys.path.append('logica/Extracao/atividades/orientacoes/')
sys.path.append('logica/Extracao/atividades/eventos/')
sys.path.append('logica/Extracao/atividades/ext/atuacaoProfissional')
sys.path.append('logica/Extracao/atividades/ext/Bancas')
sys.path.append('logica/Extracao/atividades/ext/')
sys.path.append('acesso/')
sys.path.append('acesso/Registro/')
sys.path.append('acesso/Registro/apiSql/')


from controladorExtracao import *

if __name__ == "__main__":

	arquivoConfiguracao = sys.argv[1]
	# Carrega a lista de IDs para a busca a partir de arquivo texto
	extracao = ControladorExtracao(arquivoConfiguracao)
	
	if criarDiretorio(extracao.obterParametro('global-diretorio_de_saida')):
		extracao.importarRelatorioAtividadeDocente() 
		
# ---------------------------------------------------------------------------- #
def criarDiretorio(dir):
	if not os.path.exists(dir):
		try:
			os.makedirs(dir)
		### except OSError as exc:
		except:
			return 0
	return 1

