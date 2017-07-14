#!/usr/bin/env python
#-*-coding: utf-8-*-
# Fé em Deus
#
# * Este módulo faz a leitura de um arquivo pcap e:
#	-> conta quantos pacotes smtp possui;
# 	-> ordena os pacotes smtp, remove os duplicados;
#	-> verifica se são emails que contem texto/mensagem,
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # Apenas para suprimir uma mensagem de warning
from scapy.all import * # Importando a scapy
from datetime import datetime
import sys, time, os
import csv

# Classe cores apenas para imprimir colorido no terminal
# A sintaxe é a seguinte:
# print cores.lilas + "frase colorida" + cores.fim
class cores:
    lilas = '\033[95m'
    azul = '\033[94m'
    verd = '\033[92m'
    amar = '\033[93m'
    verm = '\033[91m'
    negr = '\033[1m'
    subl = '\033[4m'
    fim = '\033[0m'

# Inicializando as variáveis
qtd_pacotes = 0
qtd_smtp = 0
emails = []

def filtrar_smtp(pacotes):
	global qtd_pacotes
	global qtd_smtp
	global emails

	# Percorrendo os pacotes
	for pacote in pacotes:
	    try:
	    	# Contado quantos pacotes são SMTP
	        if pacote[TCP].dport == 25 or pacote[TCP].sport == 25:
	        	qtd_smtp += 1
	        	# Guardando os pacotes em uma lista
	        	emails.append(pacote)
	        # str(p[Raw].load) |É o mesmo que| str(p[TCP].payload)
	        # ou seja:
	        # str(p[Raw].load) == str(p[TCP].payload)
	    except IndexError:
	        pass
	    qtd_pacotes += 1

	sys.stdout.write('\r')
	sys.stdout.write("Total = %d" % qtd_pacotes)
	sys.stdout.write("\t%s SMTP = %d%s" % (cores.verd, qtd_smtp, cores.fim,))
	sys.stdout.flush()

def processar():
	"""Função que ordena os pacotes, remove pacotes duplicados,
	define se os pacotes formam um email."""
	contador = 0
	c = 0
	# retorna um dicionario com as sessões/fluxos
	# Essa funcao do scapy é que ordena pelo numero de sequencia
	sessoes = PacketList(emails).sessions() 
	# número de sessoes/fluxos
	#print len(sessoes)
	# Criando um arquivo.csv
	capturados = "capturados.csv"#+hora+".csv"
	arquivo_csv = open(capturados, "w")
	# formato da linha csv:	rotulo,indice,"conteudo do email",dataset,arquivo
	# os dados que não são conhecidos, definimos como null apenas para
	# manter o padrão do arquivo .csv original.			
	# Escrevendo o cabeçalho no arquivo csv
	# arquivo_csv.write("label,index,msg,dataset,file\n")
	# percorrendo cada sessao/fluxo
	# dicionarios são compostos por {chave, valor}
	for key, sessao in sessoes.iteritems():
		dados = ""
		# a sessao pode ter pacotes duplicados
		# (retransmissoes)
		pacotes_unicos = []
		# Crio uma lista com os numeros de sequencia
		# percorro os pacotes. Se nao ja existir numero de
		# sequencia, adiciona o pacote na lista de unicos
		seq_unicos = set()
		for pacote in sessao:
			if not pacote[TCP].seq in seq_unicos:
				seq_unicos.add(pacote[TCP].seq)
				pacotes_unicos.append(pacote)
		for pacote in pacotes_unicos:
			try:
				dados += pacote[Raw].load
				#print dados
			except IndexError:
				pass

		# Filtrando só os dados relevantes do email
		if "Content-Type:" in dados and "MIME-Version: " in dados and "Subject: " in dados:
			try:
				remetente = dados.split("mail FROM:<")[1].split(">")[0] # testes
				destinatario = dados.split("rcpt TO:<")[1].split(">")[0] # testes
			except IndexError, ie:
				remetente = dados.split("Remetente <")[1].split(">")[0] # testes
				destinatario = dados.split("Destinatario <")[1].split(">")[0] # testes
				
			texto = "Subject: "
			texto += dados.split("Subject: ")[1] # testes
			texto = "\n".join(texto.split("\n")[:-3]) # remove as 3 ultimas linhas

			# Escrevendo conteudo dos emails em arquivos .txt
			arquivo_texto = open(nova_pasta+"/email_"+str(contador)+".txt", "w")
			arquivo_texto.write(texto)
			arquivo_texto.close()

			# Escrevendo conteúdo dos emails em arquivos .csv
			# formato da linha csv:	rotulo,indice,"conteudo do email",dataset,arquivo
			# os dados que não são conhecidos, definimos como null apenas para
			# manter o padrão do arquivo .csv original
			# o arquivo_csv é aberto fora do loop, e fechado fora do loop.
			linha  = "null,%s,'%s',null,%s,%s" % (contador, texto.replace("\r", "").replace("\n", " ").replace(",", " ").replace("'", ""), destinatario, remetente)
			linha += "\n"

			arquivo_csv.write(linha)
			sys.stdout.write('\r')
			sys.stdout.write("Salvando %s%d%s emails..." % (cores.verd, (contador+1), cores.fim,))
			sys.stdout.flush()
			contador += 1
		else:
			#print "Provavelmente nao tem texto --->"
			#print dados
			pass
	arquivo_csv.close()

	print "Dados CSV salvos em %scapturados.csv%s" % (cores.verd, cores.fim) 
	return contador,nova_pasta

# Função ler equivalente a função main
def ler():
	
	print "Arquivos disponíveis na pasta atual:\n"
	os.system("""ls -lh *.pcap | awk -F" " '{print $9, $5}' """)
	print "\nPasse o caminho do arquivo de captura:"
	caminho = raw_input('> ')
	print "\nLendo pacotes do arquivo de captura...\n"
	sniff(offline=caminho,prn=filtrar_smtp, store=0)
	print "\n"
	return processar()

if __name__ == '__main__':
	ler()
#ler()
