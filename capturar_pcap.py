#!/usr/bin/env python
#-*-coding: utf-8-*-
# Fé em Deus
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # Apenas para suprimir uma mensagem de warning
from scapy.all import * # Importando a scapy
import sys
import time
import os
import socket
from subprocess import Popen, PIPE
# Função para mostrar como deve ser chamado o programa 
def ajuda():
    print "%s v0" % sys.argv[0]
    print
    print "Uso: %s <nome_do_arquivo.pcap>" % sys.argv[0]
    print

# Se não passar 1 parâmetro, mostra ajuda e encerra o programa
if len(sys.argv) < 2:
    ajuda()
    exit(1)

def obter_tamanho(arquivo):
	processo = Popen(["ls -lh " + arquivo + "| awk -F ' ' '{print $5}' "], stdout=PIPE, shell=True)
	saida, erro = processo.communicate()
	return saida

def main():
	try:
		print "Capturando pacotes... Aperte CTRL + C para encerrr."
		os.system("echo inicio captura: $(date +%H:%M:%S) >> log.txt")
		pacotes = sniff(count=0) 
		os.system("echo fim captura: $(date +%H:%M:%S) >> log.txt")
		os.system("echo inicio escrita pcap: $(date +%H:%M:%S) >> log.txt")
		arquivo = str(sys.argv[1]) 
		wrpcap(arquivo, pacotes) 
		os.system("echo fim escrita pcap: $(date +%H:%M:%S) >> log.txt")
		tamanho = obter_tamanho(arquivo).replace("\n", "")
		print "\nCaptura encerrada. Salvo em %s. (%s)" % (arquivo, tamanho)
		#os.system("mplayer aleluia.mp3 > /dev/null 2> /dev/null")

	except socket.error:
		print
		print "Erro: Precisa ser executado com sudo."
		print
	
if __name__ == '__main__':
	main()
