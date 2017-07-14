#!/usr/bin/env python
#coding: utf-8
# Fé em Deus
from random import shuffle
import codecs
from subprocess import Popen, PIPE
import os, time
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

def executar(cmd):
	processo = Popen([cmd], stdout=PIPE, shell=True)
	saida, erro = processo.communicate()
	return saida
	
class cores:
    lilas = '\033[95m'
    azul = '\033[94m'
    verd = '\033[92m'
    amar = '\033[93m'
    verm = '\033[91m'
    negr = '\033[1m'
    subl = '\033[4m'
    fim = '\033[0m'

r = raw_input("Separa o dataset irá remover os arquivos anteriores. \nContinuar? S/N: ")
if r.lower() != "s":
	sys.exit(1)


print "Removendo arquivos anteriores..."
for i in range(10):
	executar("rm -rv enviar%d/ 2> /dev/null" % i)
	executar("rm aprender%d.csv 2> /dev/null" % i)
	executar("rm gabarito%d.csv 2> /dev/null" % i)


arquivos = os.listdir("dataset/")
shuffle(arquivos) # Embaralhado arquivos apenas UMA vez

# Definindo quem vai ser conjunto de TESTE
# Conjunto de teste deve ser maior que o de conjunto treino
teste_0 = arquivos[3370:] # done
teste_1 = arquivos[:3370] + arquivos[6740:] # done  
teste_2 = arquivos[:6740] + arquivos[10110:] # done
teste_3 = arquivos[:10110] + arquivos[13480:] # done
teste_4 = arquivos[:13480] + arquivos[16850:] # done
teste_5 = arquivos[:16850] + arquivos[20220:] # done
teste_6 = arquivos[:20220] + arquivos[23590:] # done
teste_7 = arquivos[:23590] + arquivos[26960:] # done
teste_8 = arquivos[:26960] + arquivos[30330:] # done
teste_9 = arquivos[:30330] # done

lista_de_testes = [ 
teste_0,
teste_1,
teste_2,
teste_3,
teste_4,
teste_5,
teste_6,
teste_7,
teste_8,
teste_9, ]

# Definindo quem vai ser conjunto de TREINO
# Conjunto de treino deve ser menor que o de conjunto de testes
treino_0 = arquivos[:3370] # done
treino_1 = arquivos[3370:6740] # done
treino_2 = arquivos[6740:10110] 
treino_3 = arquivos[10110:13480] 
treino_4 = arquivos[13480:16850] 
treino_5 = arquivos[16850:20220] 
treino_6 = arquivos[20220:23590] 
treino_7 = arquivos[23590:26960] 
treino_8 = arquivos[26960:30330] 
treino_9 = arquivos[30330:] 

lista_de_treinos = [ 
treino_0,
treino_1,
treino_2,
treino_3,
treino_4,
treino_5,
treino_6,
treino_7,
treino_8,
treino_9, ]

# Percorrendo as listas dos conjuntos de treino e de teste
for i in range(10):
	# COJUNTO DE TREINO
	print "\nCriando conjunto de TREINO %d..." % i
	# Bloco de código que escreve o arquivo CSV para o conjunto de treino
	aprender = codecs.open("aprender%d.csv" % i, "w")#, "ISO-8859-1")
	cont = 0
	erro = 0
	for arquivo in lista_de_treinos[i]: 
		try:	
			arquivo_txt = open("dataset/%s" % arquivo, "r")
			texto = arquivo_txt.read()
			rotulo = arquivo.split(".")[3]
			indice = cont
			conteudo = texto.replace("\r", "").replace("\n", " ")
			dataset = "1"
			arquivo = arquivo
			linha = '%s,%s,"%s",%s,%s\n' % (rotulo, indice, conteudo, dataset, arquivo)
			linha =  linha
			aprender.write(linha)
			
			###
			sys.stdout.write("\rEscrevendo %s%d%s linhas para o conjunto de treino..." % (cores.verd, cont, cores.fim))
			sys.stdout.flush()
			cont += 1
			###
		except IOError:
			erro += 1
			print "%s erros de arquivo não encontrado: %s" % (erro, arquivo)
	print "\nSalvo em %saprender%d.csv%s." % (cores.verd, i, cores.fim)
	aprender.close()


	# CONJUNTO DE TESTE
	print "\nCriando conjunto de TESTE %d..." % i
	executar("mkdir enviar%d/ 2> /dev/null" %  i)
	cont = 1
	gabarito = open("gabarito%d.csv" % i, "w") # Criando gabarito.csv
	for arquivo in lista_de_testes[i]: 
		executar("cp dataset/%s enviar%d/ 2> /dev/null > /dev/null" % (arquivo, i))
		rotulo = arquivo.split(".")[3]
		nome = arquivo
		linha = "%s,%s\n" % (rotulo, nome)
		gabarito.write(linha)

		###
		sys.stdout.write("\rMovendo %s%d%s arquivos para o conjunto de teste..." % (cores.verd, cont, cores.fim))
		sys.stdout.flush()
		cont += 1
		###
	print "\nArquivos movidos para a pasta %senviar%d/%s." % (cores.verd, i, cores.fim)
	print "Respostas salvas no arquivo %sgabarito%d.csv%s." % (cores.verd, i, cores.fim)
	gabarito.close()
	