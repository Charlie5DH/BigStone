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
#from csv2json import convert, load_csv, save_json

# Global lib imports
from _server_http import *

sys.path.insert(0,  os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from _get_ip_addr import *
from process_data import *

PORT_HTTP = 4567
I = ""

DB_TIME_OUT=400

class ServerCantina():

	def __init__(self, ip, enviroment, inicial):

		self.ip = ip
		self.file_log = ''
		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()

		signal.signal(signal.SIGINT, self.signal_handler)
		self.thr_http = reactor.callInThread(self.http_run)

		print("log em: " + self.file_log)
		logging.info("servidor de dados da Cantina inicializado")


		self.db = ProcessaDados(enviroment,logging)
		self.hasdata = 0

		# carga inicial:
		#  zera o banco e carrega saldos a partir da tabela Entradas Registradas que estiver vigente
		if inicial:
			self.db.dropDBBalance()

		self.db.popula_tabela_saldos(inicial)
		

	def load_settings(self):

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)


	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.DEBUG)

		self.file_log = "/".join((log_path,"serverCantina.log"))

		handler = logging.handlers.RotatingFileHandler(self.file_log, maxBytes=1000000, backupCount=100)
		handler.setLevel(logging.DEBUG)
 
		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)


	def handle_request(self, request):
		message = "You requested %s\n" % request.uri
		request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
		request.finish()

	def http_run(self, port=PORT_HTTP):

		try:
			logging.info("http: " + str(port))
			logging.info("Serving at: http://%(interface)s:%(port)s" % dict(interface=self.ip or "localhost", port=PORT_HTTP))
			
			application = tornado.web.Application([
				(r"/(.*)", AppHandler, dict(obj=self)),
			])
			application.listen(PORT_HTTP)
			tornado.ioloop.IOLoop.instance().start()

		except Exception as e:
			logging.info("Erro ao iniciar o servidor http: " + str(e))

	
	def signal_handler(self, signal, frame):
		logging.info('You pressed Ctrl+C!')
		reactor.stop()
		sys.exit(0)

	def transmite_tabela_dados(self, table):
		if self.hasdata > DB_TIME_OUT:
			self.db.db_reinit("Reinicia conexao com banco. Mais de " + str(DB_TIME_OUT) + " segundos sem qualquer requisicao")
		self.hasdata = 0

		logging.info("Transmite_tabela_dados: " + table)

		if table == "Saldo_Cliente":
			return self.db.getBalanceDataTable()

		if table != self.db.INPUT_TABLE_NAME:
			return self.db.getDataTable(table)

		logging.info("Não processou a tabela")

	def processa_dados_recebidos(self, data):
		if self.hasdata > DB_TIME_OUT:
			self.db.db_reinit("Reinicia conexao com banco. Mais de " + str(DB_TIME_OUT) + " segundos sem qualquer requisicao")
		self.hasdata = 0

		try:
			json_data = json.loads(data)
			for table, value in json_data.items():
				if value is not None:
					# self.db.processa_tabela(table,value)
					# self.salva_db_arq_csv(table)

					if table == self.db.INPUT_TABLE_NAME:

						self.db.processa_tabela(table,value)
						self.salva_db_arq_csv(table)

						logging.info('Atualizando saldos dos clientes')
						self.db.popula_tabela_saldos()

					elif table == self.db.PRODUCTS_TABLE_NAME:
						self.db.processa_tabela(table,value)

					else:
						logging.info("Nao processa a tabela " + table)
						logging.info(value)

			return True

		except  Exception as e:
			logging.info( "Erro no processamento de dados: " + str(e))
			return False

	def getDateLastEventEntradasRegistradas(self):
		return self.db.getDateLastEventEntradasRegistradas()

	def salva_db_arq_csv (self, table):
		dados = self.db.getDataTableToCsv(table)

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

	enviroment = 'production'
	interface="eth0"
	inicial = False
	if len(sys.argv) == 3:
		interface = sys.argv[1]
		enviroment = 'development'
		inicial = True

	ip = get_ip(interface)
	print("Escutando na interface ", interface, " ip: ", ip, " port: ", PORT_HTTP)

	sistema = ServerCantina(ip, enviroment, inicial)
	sistema.run()

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print("KeyboardInterrupt")
		reactor.stop()

