#!/usr/bin/env python
#coding: utf-8
# escrito em 01/02/2017
from subprocess import Popen, PIPE
import smtpd
import asyncore
import os

def executar_comando(comando):
	processo = Popen([comando], stdout=PIPE, shell=True)
	saida, erro = processo.communicate()
	return saida

executar_comando("fuser -k 25/tcp > /dev/null")

contador = 0

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        global contador
        contador += 1
        print 'Endereço :', peer
        print 'De       :', mailfrom
        print 'Para     :', rcpttos
        print 'Tamanho  :', len(data)
        print 'Mensagem :'
        print data
        print
        print "Total de mensagens recebidas:", contador
        print "-"*int(executar_comando("tput cols"))
        return

server = CustomSMTPServer(('127.0.0.1', 25), None)

colunas = int(executar_comando("tput cols"))

print
print (" Servidor SMTP executando ".center(colunas, "-"))
print

asyncore.loop()
