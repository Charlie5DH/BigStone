#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import signal, os
import datetime, time
import sys
import requests
import json

PORT_HTTP = 4567
I = ""

class SyncDataServer():

	def __init__(self, url, logging = None):

		self.logging = logging
		self.log ("GetDataFromServer: " + str(url))
		self.url_server = url + ":" + str(PORT_HTTP)
		self.log(self.url_server)


	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print msg

	def getData(self,table):
		self.log("Buscando tabela: " + table)

		try:

			result = requests.post(self.url_server, data="IMPORTAR:" + table, timeout=10)

			self.log("Resultado: " + str(result.status_code))

			if result.status_code == 200:
				self.log("Sucesso")
				return json.loads(result.text)

		except Exception as e:
			self.log("Erro na conexao: " + str (e))

		return None

	def setData(self,table, data):
		self.log("Tranmitindo dados para a tabela: " + table)

		try:
			result = requests.post(self.url_server, data=json.dumps(data), timeout=10)

			# self.log("Resultado: " + str(result.status_code))

			if result.status_code == 200:
				self.log("Sucesso")
				return True

		except Exception as e:
			self.log("Erro na conexao: " + str (e))

		return False


if __name__ == '__main__':

	if len(sys.argv) > 1:
		interface = sys.argv[1]

	print "Pegando dados do Servidor"
	data = SyncDataServer('http://localhost')
	data.getData("Clientes")
