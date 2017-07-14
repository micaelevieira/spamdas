#!/usr/bin/env python
#coding: utf-8
# escrito em 01/02/2017
import smtplib
import email.utils
from email.mime.text import MIMEText
import os, time, random
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
time.sleep(2)
start = time.time()

spammers = [
"shane@atkinson",
"serdar@argic",
"rolfe@larson",
"canter@siegel",
"richard@colbert",
"david@damato",
"eddie@davidson",
"peter@francismacrae",
"davis@wolfganghawke",
"jumpstart@technologies",
"vardan@kushnir",
"oleg@nikolaenko",
"ryan@pitylak",
"alan@ralsky", 
"dave@rhodes",
"scott@richter",
"sam@bruns",
"russian@businessnetwork",
"christopher@rizlersmith",
"jody@michaelsmith",
"robert@alansoloway",
"gary@thuerk",
"sanford@wallace"
]



def enviar_email(assunto, mensagem, remetente, destinatario_arquivo):
	# Criando a mensagem
	msg = MIMEText(mensagem)
	msg['To'] = email.utils.formataddr(('Destinatario', destinatario_arquivo))
	msg['From'] = email.utils.formataddr(('Remetente', remetente))
	msg['Subject'] = assunto
	#msg["Cc"] = "teste"

	server = smtplib.SMTP('127.0.0.1', 1025)
	server.set_debuglevel(True) # Mostrar a comunicação com o servidor
	try:
	    server.sendmail(remetente, [destinatario_arquivo], msg.as_string())
	finally:
	    server.quit()

# Enviando
emails = os.listdir(sys.argv[1])
for e in emails:
	arquivo = open(sys.argv[1]+e, 'r')
	nome = e
	rotulo = e.split('.')[3]
	#print "rotulo-> ", rotulo
	remetente = "remetente@exemplo"
	if rotulo == "spam":
		moeda = random.randint(1,10)
		if (moeda > 2):
			#print "spammer enviando spam"
			remetente = random.choice(spammers)
		else:
			#print "hammer enviando spam"
			remetente = "remetente@exemplo"
	elif rotulo == "ham":
		moeda = random.randint(1,10)
		if (moeda <= 2):
			#print "spammer enviando ham"
			remetente = random.choice(spammers)
		else:
			#print "hammer enviando ham
			remetente = "remetente@exemplo"

	assunto = arquivo.readline().split("Subject: ")[1] # o assunto é apenas a primeira linha
	mensagem = "".join(arquivo.readlines()[1:]) # a mensagem é a partir da segunda linha
	arquivo.close()

	enviar_email(assunto, mensagem, remetente, nome)
	time.sleep(0.1)

end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
tempo =  "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
os.system("echo Tempo de execução do enviar_emails.py: %s >> log.txt" % tempo)
