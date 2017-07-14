#!/usr/bin/env python
#coding: utf-8
import time, csv, sklearn, pandas, os, sys
from datetime import datetime
reload(sys)  
sys.setdefaultencoding('utf8')

palavras_chave = [
"bucks", "sex", "viagra", "free","urgent",
"stop", "offer", "offers", "4u", "credit cards",
"winner", "buy", "buying", "call now", "cash bonus",
"cash", "casino", "click below", "click here", "earn per week",
"instant access", "get paid", "join us", "lose weight", "lowest price",
"meet singles", "only $", "order now", "save $", "porn"
"babes","xxx" ]

class cores:
    lilas = '\033[95m'
    azul = '\033[94m'
    verd = '\033[92m'
    amar = '\033[93m'
    verm = '\033[91m'
    negr = '\033[1m'
    subl = '\033[4m'
    fim = '\033[0m'

def variacoes(palavra):
	palavras = []

	letras = {
		"a": ["@","4"],
		"e": ["3"],
		"i": ["1", "!"],
		"o": ["0"],
		"u": ["v"],
		"s": ["5"],
		"g": ["6", "9"],
		"t": ["7"],
		"z": ["2"],
		}

	# Pegando o tamanho do maior indice, para fazer um loop
	# com esse numero de interações
	tamanho_indices = []
	for l in letras:
		tamanho = len(letras.get(l))
		tamanho_indices.append(tamanho)
	tamanho_indices = max(tamanho_indices) 

	# Percorrendo a palavra e substituindo as letras
	i = 0
	while i < tamanho_indices:
		for l in letras:
			try:
				palavra_tmp = palavra.replace(l, letras.get(l)[i])
				palavras.append(palavra_tmp)
			except IndexError, msg:
				palavras.append(palavra_tmp)
		i += 1

	# Percorrendo as novas palavras e substituindo as letras
	novas_palavras = []
	for p in palavras:
		i = 0
		while i < tamanho_indices:
			for l in letras:
				try:
					palavra_tmp = p.replace(l, letras.get(l)[i])
					novas_palavras.append(palavra_tmp)
				except IndexError, msg:
					novas_palavras.append(palavra_tmp)
			i += 1

	palavras_finais = palavras + novas_palavras
	palavras_unicas = list(set(palavras_finais))

	novas_palavras = []
	novas_palavras += palavras_unicas

	# Criando palavras com ponto entre as letras
	for palavra in palavras_unicas:
		palavra_ponto = ".".join(list(palavra))
		#print palavra_ponto
		novas_palavras.append(palavra_ponto)

	novas_palavras2 = []
	novas_palavras2 += novas_palavras

	# Criando palavras com espaço entre as letras
	for palavra in novas_palavras:
		palavra_espaco = " ".join(list(palavra))
		novas_palavras2.append(palavra_espaco)

	# Criando palavras com espaço e ponto entre as letras
	for palavra in palavras_unicas:
		palavra_espaco = " ".join(list(palavra))
		novas_palavras.append(palavra_espaco)

	return novas_palavras2

def demonstracao():
	start = time.time()
	print "Executando Palavras Chave..."
	print "Carregando dados dos arquivos CSV..."
	emails_capturados = pandas.read_csv('capturados.csv', sep=',', usecols=[0,2,4], quotechar='"',
	                           names=["rotulo", "conteudo", "nome_arquivo"])#), "message","dataset","file"])

	respostas = pandas.read_csv('gabarito.csv', sep=',', usecols=[0,1], quotechar='"',
	                           names=["rotulo", "nome_arquivo"])#), "message","dataset","file"])

	# Sincronizando as listas, deixando-as na mesma ordem
	tamanho_antes = len(respostas)
	#time.sleep(1)
	respostas = respostas[respostas["nome_arquivo"].isin(emails_capturados["nome_arquivo"])]
	tamanho_depois = len(respostas)
	#stime.sleep(1)
	emails_perdidos = tamanho_antes - tamanho_depois
	print "%d emails perdidos." % emails_perdidos
	time.sleep(1)
	emails_capturados = emails_capturados.sort_values(["nome_arquivo"])
	respostas = respostas.sort_values(["nome_arquivo"])

	acertos = 0
	spams = 0
	hams = 0
	total = 0
	fp = 0 # Falso Positivo
	fn = 0 # Falso Negativo
	vp = 0 # Verdadeiro Positivo
	vn = 0 # Verdadeiro Negativo

	for email, resposta, nome_gabarito, arquivo in \
	 zip(emails_capturados['conteudo'],
	 	respostas["rotulo"],
	 	respostas["nome_arquivo"],
	 	emails_capturados["nome_arquivo"]):	

	 	# Checando se é o mesmo que foi enviado
		if not nome_gabarito == arquivo:
		    print "Erro: Listas não estão sincronizadas ou não são a mesma lista."
			
		total += 1
		#time.sleep(0.1)
		
		pc = "ham"
		chave = "\t"
		for palavra in palavras_chave:
			for variacao in variacoes(palavra):
				if variacao in email:
					chave = variacao+"\t"
					pc = "spam"
					break

		porcentagem = round((float(acertos)/total)*100.0, 2)
		
		# falso positivo, falso negativo, verdadeiro positivo, verdadeiro negativo
		if resposta == "ham" and resposta == pc:
			vp += 1
		if resposta == "spam" and resposta == pc:
			vn += 1
		if resposta == "ham" and resposta != pc:
			fp += 1
		if resposta == "spam" and resposta != pc:
			fn += 1

		if resposta == "ham":
			hams += 1
		if resposta == "spam":
			spams += 1
		if pc == resposta: # pc = retorno da tecnica palavras-chave
			acertos += 1
			print "Palavras-Chave: %s%s%s\t Correto: %s%s%s\t %s %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verd, pc, cores.fim, cores.verd, resposta, cores.fim, chave, arquivo, acertos, porcentagem, "%")
		else:
			print "Palavras-Chave: %s%s%s\t Correto: %s%s%s\t %s %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verm, pc, cores.fim, cores.verm, resposta, cores.fim, chave, arquivo, acertos, porcentagem, "%")
			
	print "Total " + str(total) + "\t Acertos: " + str(acertos) + " (" + str(porcentagem)+ ")"

	arquivo = open("resultados.txt", "a")
	data = datetime.now().strftime('%d-%m-%Y')
	hora = datetime.now().strftime('%H:%M:%S')
	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	tempo =  "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	resultado = """============================
Resultado - Palavras Chave
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
