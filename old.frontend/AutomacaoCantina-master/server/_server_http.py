#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json, pprint
from serverCantina import *

class AppHandler(tornado.web.RequestHandler):
	def get(self, data):
		uri = self.request.uri
		# print uri + " -> " + data

	def post(self, data):
		
		data = self.request.body
		#logging.info ( "BODY: "+ str (data))

		uri = self.request.uri
		logging.info ( "URI: " + str(uri))

		#try:
		length  = int(self.request.headers.get("Content-Length",0))
		self.set_header('Content-type', 'text/html')

		cmd = ""
		if len(data) < 100: 
			cmd,table=data.split(":")

		logging.info ( "OPERACAO: " + str(cmd))
		if cmd == "STATUS":
			data_last_event = self.objapp.getDateLastEventEntradasRegistradas()
			self.write(str(data_last_event))

		elif cmd == "IMPORTAR":
			logging.info ("Recebido comando: ")
			logging.info (data)

			j = self.objapp.transmite_tabela_dados(table)
			#logging.info (j)
			self.write(j)
		else:
			if self.objapp.processa_dados_recebidos(data):
				self.write("Dados recebidos com sucesso")
			else:
				self.write("Falha")

		#except Exception as exc:
		#	logging.error("{0}/{1}({2})".format(type(self).__name__, type(exc).__name__, str(exc)))
		

	def initialize(self, obj):
		self.objapp = obj
