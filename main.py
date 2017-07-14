#!/usr/bin/env python
#-*-coding: utf-8-*-
# Fé em Deus
from ler_pcap import ler
import nb, svm, listas_negras, palavras_chave
import os, sys

def main():
	os.system("figlet 'spamdas v0.1'")
	print "Bem vindo ao spamdas! Versão de demonstração."
	ler()
        os.system("mplayer moeda.mp3 > /dev/null 2> /dev/null")
        sys.exit(1)


	while True:

		print '''
Escolha uma opção:

1 - Listas Negras
2 - Palavras Chaves
3 - Naive Bayes
4 - SVM
5 - Todas as técnicas
6 - Escolher outro trace
7 - Sair
'''

		opcao = input('> ')
		if (opcao==1): # Listas Negras
			listas_negras.demonstracao()
		elif (opcao==2): # Palavras Chaves
			palavras_chave.demonstracao()
		elif (opcao==3): # Palavras Chaves
			nb.demonstracao()
		elif(opcao==4): # SVM
			svm.demonstracao()
		elif(opcao==5): # Todas as tecnicas
			listas_negras.demonstracao()
			palavras_chave.demonstracao()
			nb.demonstracao()
			svm.demonstracao()
		elif(opcao==6): # escolher outro trace
			main() 
		elif(opcao==7):
			sys.exit()

if __name__ == '__main__':
	main()
