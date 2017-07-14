#!/usr/bin/env python
#coding: utf-8
# Fé em Deus
#import matplotlib.pyplot as plt
#import numpy as np
#from sklearn.svm import SVC, LinearSVC
#from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
#from sklearn.tree import DecisionTreeClassifier 
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedKFold, cross_val_score, train_test_split 
import time, sklearn, pandas
from datetime import datetime
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class cores:
    lilas = '\033[95m'
    azul = '\033[94m'
    verd = '\033[92m'
    amar = '\033[93m'
    verm = '\033[91m'
    negr = '\033[1m'
    subl = '\033[4m'
    fim = '\033[0m'

def split_into_tokens(message):
	
	message = message.decode('utf-8','ignore').encode("utf-8")  
	return TextBlob(message).words

def split_into_lemmas(message):
	try:
		message = unicode(message, 'utf8')
		words = TextBlob(message).words
		return [word.lemma for word in words]
	except UnicodeDecodeError, msg:
		pass
    
def demonstracao():
	start = time.time()
	print "Executando Naive Bayes..."
	print "Carregando dados dos arquivos CSV..."
	messages = pandas.read_csv('aprender.csv', sep=',', usecols=[0,2], quotechar='"',
	                           names=["rotulo", "conteudo"])#), "message","dataset","file"])

	emails_capturados = pandas.read_csv('capturados.csv', sep=',', usecols=[0,2,4], quotechar='"',
	                           names=["rotulo", "conteudo", "nome_arquivo"])#), "message","dataset","file"])

	respostas = pandas.read_csv('gabarito.csv', sep=',', usecols=[0,1], quotechar='"',
	                           names=["rotulo", "nome_arquivo"])#), "message","dataset","file"])

	# Sincronizando as listas, deixando-as na mesma ordem
	tamanho_antes = len(respostas)
	#print tamanho_antes
    #    time.sleep(1)
	respostas = respostas[respostas["nome_arquivo"].isin(emails_capturados["nome_arquivo"])]
	tamanho_depois = len(respostas)
    #    print tamanho_depois
    #    time.sleep(1)
	emails_perdidos = tamanho_antes - tamanho_depois
	print "%d emails perdidos." % emails_perdidos
	time.sleep(1)
	emails_capturados = emails_capturados.sort_values(["nome_arquivo"])
	respostas = respostas.sort_values(["nome_arquivo"])

	print "Separando dados para aprendizagem..."
	msg_train, msg_test, label_train, label_test = \
	    train_test_split(messages['conteudo'], messages['rotulo'], test_size=0.2)

	pipeline = Pipeline([
	    ('bow', CountVectorizer(analyzer=split_into_lemmas)),  # contador inteiro de strings para tokens
	    ('tfidf', TfidfTransformer()),  
	    ('classifier', MultinomialNB()),  # treinar vetores TF-IDF com o classificador Naive Bayes
		])

	print "Treinando..."
	scores = cross_val_score(pipeline,  
                                 msg_train,  
	                         label_train,  
	                         cv=10,  
	                         n_jobs=1, 
	                         )

	params = {
	    'tfidf__use_idf': (True, False),
	    'bow__analyzer': (split_into_lemmas, split_into_tokens),
	}

	grid = GridSearchCV(
	    pipeline,  
	    params,  
	    refit=True, 
	    n_jobs=-1,  
	    cv=StratifiedKFold(label_train, n_folds=5),  
	)

	print "Realizando classificação..."
	nb_detector = grid.fit(msg_train, label_train)
	
	acertos = 0
	spams = 0
	hams = 0
	total = 0
	fp = 0 # Falso Positivo
	fn = 0 # Falso Negativo
	vp = 0 # Verdadeiro Positivo
	vn = 0 # Verdadeiro Negativo
	#print emails_capturados["nome_arquivo"]
	#time.sleep(5)

	for email, resposta, nome_gabarito, arquivo in \
	 zip(emails_capturados['conteudo'],
	 	respostas["rotulo"],
	 	respostas["nome_arquivo"],
	 	emails_capturados["nome_arquivo"]):	

	 	#print nome_gabarito == arquivo
	 	#time.sleep(1) 

	 	# Checando se é o mesmo que foi enviado
		if not nome_gabarito == arquivo:
			print nome_gabarito
			print arquivo
			print "Algo de errado nao esta certo"
			time.sleep(10)

		total += 1
		#time.sleep(0.1)
		porcentagem = round((float(acertos)/total)*100.0, 2)
		nb = nb_detector.predict([email])[0]

		# falso positivo, falso negativo, verdadeiro positivo, verdadeiro negativo
		if resposta == "ham" and resposta == nb:
			vp += 1
		if resposta == "spam" and resposta == nb:
			vn += 1
		if resposta == "ham" and resposta != nb:
			fp += 1
		if resposta == "spam" and resposta != nb:
			fn += 1

		if resposta == "ham":
			hams += 1
		if resposta == "spam":
			spams += 1
		if nb == resposta:
			acertos += 1
			print "Naive Bayes: %s%s%s\t Correto: %s%s%s\t %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verd, nb, cores.fim, cores.verd, resposta, cores.fim, arquivo, acertos, porcentagem, "%")
			#print  "Acertos: " + str(acertos) + " (" + str(porcentagem)+ "%)\t  Naive Bayes: " + cores.verd + nb + cores.fim + "\t" +\
			# "Correto: " + cores.verd + resposta + cores.fim + "\t" + str(nome_gabarito) + "\t"
		else:
			print "Naive Bayes: %s%s%s\t Correto: %s%s%s\t %s \t\tAcertos: %d (%.2f%s)" \
			% (cores.verm, nb, cores.fim, cores.verm, resposta, cores.fim, arquivo, acertos, porcentagem, "%")
			#print  "Acertos: " + str(acertos) + " (" + str(porcentagem)+ "%)\t Naive Bayes: " + cores.verm + nb + cores.fim + "\t" + \
			#"Correto: " + cores.verm + resposta + cores.fim + "\t" + str(nome_gabarito) + "\t"
	
	porcentagem = round((float(acertos)/total)*100.0, 2)
	print "Total " + str(total) + "\t Acertos: " + str(acertos) + " (" + str(porcentagem)+ ")"



	arquivo = open("resultados.txt", "a")
	data = datetime.now().strftime('%d-%m-%Y')
	hora = datetime.now().strftime('%H:%M:%S')
	end = time.time()
	hours, rem = divmod(end-start, 3600)
	minutes, seconds = divmod(rem, 60)
	tempo =  "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
	resultado = """============================
Resultado - Naive Bayes
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
"""  % (data, hora, total, emails_perdidos, acertos, vp, vn, fp, fn,str(porcentagem)+'%', tempo )
	arquivo.write(resultado)
	arquivo.close()
	print "Resultados salvos em %sresultados.txt%s" % (cores.verd, cores.fim)


if __name__ == '__main__':
	demonstracao()
