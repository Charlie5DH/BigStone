#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json, pprint

from motor_envia_email import *

class AppHandler(tornado.web.RequestHandler):
	def get(self, data):
		uri = self.request.uri
		# print uri + " -> " + data

		if uri == "/get_running_messages":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_running_messages())

	def post(self, data):
		
		data = self.request.body
		logging.info ( "BODY: "+ str (data))

		uri = self.request.uri
		logging.info ( "URI: " + str(uri))

		if uri == "/despacho_email":
			self.set_header("Access-Control-Allow-Origin","*")
			data_ini = self.get_argument("dataini", None)
			envio_para = self.get_argument("enviopara", None)
			destinatario = self.get_argument("destinatario", None)

			self.write(self.objapp.inicia_despacho_email(envio_para, data_ini, destinatario))

	def initialize(self, obj):
		self.objapp = obj
