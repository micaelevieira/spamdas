#!/usr/bin/env python
#coding: utf-8
# Fé em Deus
import time, sklearn, pandas, os, sys
from datetime import datetime
start = time.time()

class cores:
    lilas = '\033[95m'
    azul = '\033[94m'
    verd = '\033[92m'
    amar = '\033[93m'
    verm = '\033[91m'
    negr = '\033[1m'
    subl = '\033[4m'
    fim = '\033[0m'

def demonstracao():
	print "Executando Listas Negras..."
	#0		1		2		3			4		5		
	#label,	index,	msg,	dataset,	file,	remetente
	emails_capturados = pandas.read_csv('capturados.csv', sep=',', usecols=[0,2,4,5], quotechar='"',
	                           names=["rotulo", "conteudo","nome_arquivo","remetente"])#), "message","dataset","file"])

	respostas = pandas.read_csv('gabarito.csv', sep=',', usecols=[0,1], quotechar='"',
	                           names=["rotulo", "nome_arquivo"])#), "message","dataset","file"])

	# Sincronizando as listas, deixando-as na mesma ordem
	tamanho_antes = len(respostas)
	#print tamanho_antes
	#time.sleep(1)
	respostas = respostas[respostas["nome_arquivo"].isin(emails_capturados["nome_arquivo"])]
	tamanho_depois = len(respostas)
	#print tamanho_depois
	#time.sleep(1)
	emails_perdidos = tamanho_antes - tamanho_depois
	print "%d emails perdidos." % emails_perdidos
	time.sleep(1)
	emails_capturados = emails_capturados.sort_values(["nome_arquivo"])
	respostas = respostas.sort_values(["nome_arquivo"])
	
	with open("blacklist.txt") as arquivo:
	    bloqueados = arquivo.read().splitlines() 

	acertos = 0
	spams = 0
	hams = 0
	total = 0
	fp = 0 # Falso Positivo
	fn = 0 # Falso Negativo
	vp = 0 # Verdadeiro Positivo
	vn = 0 # Verdadeiro Negativo

	for remetente, resposta, nome_gabarito, arquivo in \
	zip(emails_capturados['remetente'], # remetentes
		respostas["rotulo"], # spam ou ham correto
		respostas["nome_arquivo"], # do arquivo 
		emails_capturados["nome_arquivo"]):

		total += 1
		#time.sleep(0.1)

		# Checando se é o mesmo que foi enviado
		if not nome_gabarito == arquivo:
		    print "Erro: Listas não estão sincronizadas ou não são a mesma lista."
		
		# Se o remetente estiver na lista dos bloqueados
		# A lista negra deflagrou como spam
		if remetente in bloqueados:
			ln = "spam"
		else:
			ln = "ham"

		porcentagem = round((float(acertos)/total)*100.0, 2)
	
		# falso positivo, falso negativo, verdadeiro positivo, verdadeiro negativo
		if resposta == "ham" and resposta == ln:
			vp += 1
		if resposta == "spam" and resposta == ln:
			vn += 1
		if resposta == "ham" and resposta != ln:
			fp += 1
		if resposta == "spam" and resposta != ln:
			fn += 1	

		if resposta == "ham":
			hams += 1
		if resposta == "spam":
			spams += 1
		if ln == resposta:
			acertos += 1
			print "Listas Negras: %s%s%s\t Correto: %s%s%s\t %s %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verd, ln, cores.fim, cores.verd, resposta, cores.fim, remetente, arquivo, acertos, porcentagem, "%")
			#print  "Acertos: " + str(acertos) + " (" + str(porcentagem)+ "%)\t  Lista Negra: " + cores.verd + ln + cores.fim + "\t" + "Correto: " + cores.verd + resposta + cores.fim + "\t" + str(remetente) + "\t"
		else:
			print "Listas-Negras: %s%s%s\t Correto: %s%s%s\t %s %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verm, ln, cores.fim, cores.verm, resposta, cores.fim, remetente, arquivo, acertos, porcentagem, "%")
			#print  "Acertos: " + str(acertos) + " (" + str(porcentagem)+ "%)\t Lista Negra: " + cores.verm + ln + cores.fim + "\t" + "Correto: " + cores.verm + resposta + cores.fim + "\t" + str(remetente) + "\t"

	porcentagem = round((float(acertos)/total)*100.0, 2)
	print "Total " + str(total) + "\t Acertos: " + str(acertos) + " (" + str(porcentagem)+ "%)"

	
	arquivo = open("resultados.txt", "a")
	data = datetime.now().strftime('%d-%m-%Y')
	hora = datetime.now().strftime('%H:%M:%S')
	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	tempo =  "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	resultado = """============================
Resultado - Listas Negras
Data: %s Hora: %s
Total de emails: %s
Emails perdidos: %s
Acertos: %s
Verdadeiro Positivos: %s
Verdadeiro Negativos: %s
Falso Positivos: %s
Falso Negativos: %s
Precisão: %s
Tempo de execução: %s
"""  % (data, hora, total, emails_perdidos, acertos, vp, vn, fp, fn, str(porcentagem)+'%', tempo)
	arquivo.write(resultado)
	arquivo.close()
	print "Resultados salvos em %sresultados.txt%s" % (cores.verd, cores.fim)


if __name__ == '__main__':
	demonstracao()