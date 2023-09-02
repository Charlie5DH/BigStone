#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json, pprint
#from controleCantina import *

class AppHandler(tornado.web.RequestHandler):
	def get(self, data):
		#mode = self.get_argument("operation")
		# print "REQ", self.request
		uri = self.request.uri

		# print uri + " -> " + data

		if uri == "/now_operation":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_NowOperation())

		if uri == "/peso":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Peso())

		if uri == "/valor":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Valor())

		if uri == "/nome":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Nome())

		if uri == "/confirma":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Confirma())

		if uri == "/cancela":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Cancela())

		if uri == "/suco":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_Suco())

		if uri == "/ip":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_IP())

		if uri == "/dados":
			self.set_header("Access-Control-Allow-Origin","*")
			self.set_header("Content-Type", "application/json; charset=utf-8")
			dados = self.objapp.get_DadosAlmoco()
			# logging.info(dados)
			self.write(dados)
		
		if uri == "/dados_lanche":
			self.set_header("Access-Control-Allow-Origin","*")
			self.set_header("Content-Type", "application/json; charset=utf-8")
			dados = self.objapp.get_DadosLanche()
			# logging.info(dados)
			self.write(dados)

		if uri == "/ultimaAtualizacao":
			self.set_header("Access-Control-Allow-Origin","*")
			self.write(self.objapp.get_UltimaAtualizacao())			

	def post(self, data):
		
		data = self.request.body
		# logging.info ( "BODY: "+ str (data))

		uri = self.request.uri
		#logging.info ( "URI: " + str(uri))

		self.set_header("Access-Control-Allow-Origin","*")

		if uri == "/suco":
			qnt = int(self.get_argument("quantidade"))
			self.write(self.objapp.set_Suco(qnt))

		if uri == "/quantidade_produto":
			self.set_header("Access-Control-Allow-Origin","*")
			qnt = int(self.get_argument("quantidade"))
			print(qnt)
			self.write(self.objapp.set_QntProduto(qnt))

		if uri == "/matricula":
			self.set_header("Access-Control-Allow-Origin","*")
			matricula = self.get_argument("matricula")
			self.write(self.objapp.set_Matricula(matricula))

		if uri == "/nome":
			self.set_header("Access-Control-Allow-Origin","*")
			nome = self.get_argument("nome")
			self.write(self.objapp.set_Nome(nome))

		if uri == "/confirma_lanche":
			self.set_header("Access-Control-Allow-Origin","*")
			nome       = self.get_argument("nome")
			manter     = self.get_argument("manter")
			self.write(self.objapp.set_ConfirmaLanche(nome.encode('utf-8'), manter))

		if uri == "/confirma_almoco":
			self.set_header("Access-Control-Allow-Origin","*")
			nome         = self.get_argument("nome")
			manter       = self.get_argument("manter")
			produto      = self.get_argument("produto")
			valor_almoco = self.get_argument("valor")
			quantidade   = self.get_argument("quantidade")
			self.write(self.objapp.set_ConfirmaLanche(nome.encode('utf-8'), manter, produto.encode('utf-8'), valor_almoco, quantidade))

		if uri == "/confirma":
			self.set_header("Access-Control-Allow-Origin","*")
			nome = self.get_argument("nome")
			self.write(self.objapp.set_Confirma(nome.encode('utf-8')))

		if uri == "/barcodeid":
			self.set_header("Access-Control-Allow-Origin","*")
			barcodeid = self.get_argument("barcodeid")
			self.write(self.objapp.set_BarCodeId(barcodeid))

		if uri == "/ip":
			self.set_header("Access-Control-Allow-Origin","*")
			ip_address = self.get_argument("ip_address")
			self.objapp.set_IP(str(ip_address))
			self.write("Ok")

		if uri == "/apaga":
			self.set_header("Access-Control-Allow-Origin","*")
			id_apaga = self.get_argument("id")
			if self.objapp.alteraEntradaRegistrada(id_apaga, "removido"):
				self.write("Ok")
			else:
				self.write("Erro")

		if uri == "/paga":
			self.set_header("Access-Control-Allow-Origin","*")
			id_paga = self.get_argument("id")
			if self.objapp.alteraEntradaRegistrada(id_paga, "pago"):
				self.write("Ok")
			else:
				self.write("Erro")
		
		if uri == "/sincroniza":
			self.set_header("Access-Control-Allow-Origin","*")
			dia_sincroniza = self.get_argument("dia")
			if self.objapp.sincronizaEntradasRegistradas(dia_sincroniza):
				self.write("Ok")
			else:
				self.write("Erro")

		if uri == "/produto":
			self.set_header("Access-Control-Allow-Origin","*")
			produto = self.get_argument("produto")
			self.write(self.objapp.set_Produto(produto.encode('utf-8')))

		if uri == "/dataevento":
			self.set_header("Access-Control-Allow-Origin","*")
			dataevento = self.get_argument("dataevento")
			self.write(self.objapp.set_DataEvento(dataevento))

	def initialize(self, obj):
		self.objapp = obj
