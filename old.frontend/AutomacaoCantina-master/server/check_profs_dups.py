#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import signal, os
import datetime, time
import sys
from twisted.internet import reactor
from twisted.internet import task
import SimpleHTTPServer
import SocketServer
import socket
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import tornado.web
import glob
import json, pprint
import shutil
import subprocess
import logging
import csv


# Global lib imports
from _server_http import *

sys.path.insert(0,  os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from _get_ip_addr import *
from process_data import *

PORT_HTTP = 4567
I = ""

DB_TIME_OUT=1400

class CheckDups():

	def __init__(self):

		self.file_log = ''
		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()

		signal.signal(signal.SIGINT, self.signal_handler)

		print "log em: " + self.file_log
		logging.info("verifica duplicados")

		self.db = ProcessaDados("development",logging)
		self.hasdata = 0

		

	def load_settings(self):

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)


	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.DEBUG)

		self.file_log = "/".join((log_path,"duplicados.log"))

		handler = logging.handlers.RotatingFileHandler(self.file_log, maxBytes=1000000, backupCount=100)
		handler.setLevel(logging.DEBUG)
 
		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	
	def signal_handler(self, signal, frame):
		logging.info('You pressed Ctrl+C!')
		reactor.stop()
		sys.exit(0)

	def verifica_tabela_dados(self,date,apaga):

		print "Dia: " + str(date)
		print "Apagar: " + str(apaga)
		entradas1 = self.db.getAllEntradasRegistradas(date)
		entradas2 = entradas1

		c=0
		en=0
		conta_e1 = 0
		for e1 in entradas1:
			conta_e1 += 1
			conta_e2 = 0
			for e2 in entradas2:
				conta_e2 += 1
				if conta_e2 <= conta_e1:
					continue

				if  e1[9] == e2[9] and \
					e1[2] == e2[2] and \
					e1[3] == e2[3] and \
					e1[4] == e2[4] and \
					e1[5] == e2[5] and \
					e1[6] == e2[6] and \
					e1[7] == e2[7]:

					if apaga:
						print "Encontrei! Vai apagar " + str(e1[0])

						if e1[8] == 'NAO':
							self.db.apagaEntradaRegistrada(e1[0])
						else:
							self.db.apagaEntradaRegistrada(e2[0])
					else:
						print "Encontrei: "
					print e1
					print e2 
					print " "
					en = en + 1
					
				c = c +1
		print "Processados: " + str(c)
		print "Duplicados: " + str (en)

	def deposita_valor_pago(self,date,deposita):

		print "Dia: " + str(date)
		print "Depositar: " + str(deposita)
		pagos = self.db.getAllEntradasRegistradasPagas(date)

		c=0
		for e1 in pagos:
			if deposita:
				# print "Encontrei! Vai depositar " + str(e1[3]) + " : " + str(e1[5])
				self.db.realizaDeposito(e1[3], e1[6], e1[5])

	
			print e1
			c = c +1
		print "Pagos: " + str(c)

	def verifica_almoco_duplicado(self,date, acao):

		print "Dia: " + str(date)
		print "Apagar: " + str(acao)
		almocos1 = self.db.getAllEntradasRegistradas(date)
		almocos2 = almocos1

		
		c=0
		conta_e1 = 0
		for e1 in almocos1:
			conta_e1 += 1
			# if e1[9] == "1":
			# 	continue

			if e1[3] == "ARTHUR CUNHA RANGEL DE SOUSA":
				continue
			if e1[8] == "SIM":
				continue

			conta_e2 = 0
			tipo_cliente = self.db.getTypeClientFromName (e1[3])
			prd = e1[4].encode('utf-8')
			if tipo_cliente == "Professor" and (prd == "Almoco" or prd == "Almoço"):

				for e2 in almocos2:
					conta_e2 += 1
					if conta_e2 <= conta_e1:
						continue

					# if e2[9] == "1": 
					# 	continue

					if  e1[9] == e2[9] and \
						e1[2] == e2[2] and \
						e1[3] == e2[3] and \
						e1[4] == e2[4] and \
						e1[6] == e2[6] and \
						e1[7] == e2[7]:
							
						if acao:
							print "Encontrei! Vai apagar " + str(e1[0])
							self.db.apagaEntradaRegistrada(e1[0])


						print e1
						print e2
						print "\n"
			c = c +1
		print "Apagados: " + str(c)

	def run(self):
		tempo_loop = 1
		self.hasdata = self.hasdata + 1

		reactor.callLater(tempo_loop, self.run)

#
# Process init
#

def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	logging.info( "Recieved signal " + str(num) + " - " + k[num])

	reactor.stop()
	os._exit(1)

if __name__ == '__main__':

	date = '18/03/2019'
	acao = False
	if len(sys.argv) == 3:
		date = sys.argv[1]
		if sys.argv[2] == '1':
			acao = True

	sistema = CheckDups()
	#sistema.verifica_tabela_dados(date,acao)
	#sistema.deposita_valor_pago (date,acao)
	sistema.verifica_almoco_duplicado (date,acao)
	

	# try:
	# 	signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
	# 	signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
	# 	reactor.run()

	# except KeyboardInterrupt:
	# 	print "KeyboardInterrupt"
	# 	reactor.stop()

