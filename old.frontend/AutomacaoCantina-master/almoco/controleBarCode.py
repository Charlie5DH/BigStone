#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests

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


# Local Classes
from _barCodeReader import *

URL = "http://localhost"
PORT_HTTP = 4567
I = ""

# Bar Code
PORT_BARCODE="/dev/hidraw0"
#PORT_BARCODE="AAAA"

class BarCode():

	def __init__(self):

		self.load_settings()

		self.url_server = URL + ":" + str(PORT_HTTP) + "/barcodeid"
		logging.info( "Controlador de Leitor de Codigo de Barras")
		self.bcStart()

	def bcStart (self):

		try:
			self.barcode = BarCodeReader(PORT_BARCODE, self.__new_barcode)
			self.barcode.getBarCode()

		except Exception, e:
			logging.info( "Falha no acesso ao leitor de código de barras")
			self.idBarCode = "FALHA_LEITOR"
			self.newBarCodeId();
			reactor.callLater(5,self.bcStart)	

	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.INFO)

		handler = logging.handlers.RotatingFileHandler("/".join((log_path,"controleBarCode.log")), maxBytes=100000, backupCount=1000)
		handler.setLevel(logging.INFO)

		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def load_settings(self):

		self.base_data_path = "."

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)

	def signal_handler(self, signal, frame):
		logging.info( 'You pressed Ctrl+C!')
		reactor.stop()
		sys.exit(0)

# Código de Barras
	def newBarCodeId(self):

		try:
			headers = {'Content-type':'application/x-www-form-urlencoded','Accept':'text/plain'}

			data_code = "barcodeid=" + str(self.idBarCode)

			r = requests.post(self.url_server, data=data_code, headers=headers, timeout=30)

			if r.status_code == 200 or  r.status_code == 201:
				logging.info( "Sucesso!")
			else:
				logging.info( r.status_code)

		except:
			logging.info( "Falha de conexao com server da cantina! Nao mandou codigo de barras.")

	def __new_barcode(self):
		self.idBarCode = self.barcode.idBarCode
		self.newBarCodeId()

		logging.info( "Done BarCode: " + str(self.idBarCode))
		reactor.callWhenRunning(self.barcode.getBarCode)

#
# Process init
#

def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	logging.info( "Recieved signal " + str(num) + " - " + k[num])

	reactor.stop()
	os._exit(1)

if __name__ == '__main__':

	print "Leitor de codigo de barras iniciando..."
	BarCode = BarCode()

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		logging.info( "KeyboardInterrupt")
		reactor.stop()

