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
from csv2json import convert, load_csv, save_json

# Local Classes
from _server_http import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from process_data import *

class IniciaSistema():

	def __init__(self):

		self.file_log = ''
		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()

		print "log em: " + self.file_log
		logging.info("Controlador de Regitros de Almoços da Cantina")


		self.db = ProcessaDados(logging)

	def load_settings(self):

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)


	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.DEBUG)

		self.file_log = "/".join((log_path,"cadastraCliente.log"))

		handler = logging.handlers.RotatingFileHandler(self.file_log, maxBytes=100000, backupCount=1000)
		handler.setLevel(logging.DEBUG)
 
		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def run(self, file_csv):

		file_json = file_csv + ".json"

		with open(file_csv) as r, open(file_json, 'w') as w:
			convert(r, w)

		with open(file_json) as data_file:
			json_data = json.load(data_file)
			self.db.processa_tabela("Clientes",json_data)

		#reactor.callLater(tempo_loop, self.run)

#
# Process init
#

def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	logging.info( "Recieved signal " + str(num) + " - " + k[num])

	reactor.stop()
	os._exit(1)

if __name__ == '__main__':

	if len(sys.argv) != 2:
		print "Informe o nome do arquivo CSV de clientes"
		os._exit(1)
		
	file_name = sys.argv[1]

	if os.path.isfile(file_name) is False:	
		print "Arquivo não existe: ", file_name
		os._exit(1)

	sistema = IniciaSistema()
	sistema.run(file_name)

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print "KeyboardInterrupt"
		reactor.stop()

