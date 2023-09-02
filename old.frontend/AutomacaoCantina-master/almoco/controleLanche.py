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

# Local Classes
from _server_http import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from process_data import *

PORT_HTTP = 4566
I = ""

class IniciaSistema():

	def __init__(self, enviroment):

		self.file_log = ''
		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()

		print("log em: " + self.file_log)

		logging.info("Controlador de Regitros de Lanches da Cantina")

		self.db = ProcessaDados(enviroment, logging)
		self.Sucesso = 10


	def load_settings(self):

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)


	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.DEBUG)

		self.file_log = "/".join((log_path,"controleLanche.log"))

		handler = logging.handlers.RotatingFileHandler(self.file_log, maxBytes=1000000, backupCount=1000)
		handler.setLevel(logging.DEBUG)

		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def run(self):
		pass

	
class ProcLanchesCantina():

	def __init__(self, system):

		self.db = system.db

		signal.signal(signal.SIGINT, self.signal_handler)
		self.thr_http = reactor.callInThread(self.http_run)

		self.resetaVariaveisOperacao()

	def resetaVariaveisOperacao (self, name=None):
		self.Valor       = None
		self.TipoCliente = None
		self.Desconto    = None
		self.Produto     = None
		self.QntProduto  = 1
		self.Nome      = name
		self.Suco      = None
		self.Confirma  = None
		self.Cancela   = None
		self.resetou = True
		self.DataEvento = None
		if self.Nome is None:
			self.Status		= None

		logging.info("Finalizou!!!")


	def handle_request(self, request):
		message = "You requested %s\n" % request.uri
		request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
		request.finish()

	def http_run(self, port=PORT_HTTP):

		try:
			logging.info("http: " + str(port))
			logging.info("Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT_HTTP))
			
			application = tornado.web.Application([
				(r"/(.*)", AppHandler, dict(obj=self)),
			])
			application.listen(PORT_HTTP)
			tornado.ioloop.IOLoop.instance().start()

		except Exception as e:
			logging.info("Erro ao iniciar o servidor http: " + str(e))

	def stop(self):
		tornado.ioloop.IOLoop.instance().stop()

	def signal_handler(self, signal, frame):
		logging.info('You pressed Ctrl+C!')
		reactor.stop()
		sys.exit(0)

	def run(self):
		pass

	def pegaDesconto(self, tipo_cliente):
		desconto = float(self.db.getDiscontoOfClientType(tipo_cliente))
		if desconto is not None:
			return desconto
			
		return 0

	def get_NowOperation(self):
		# nada
		return ("now_operation")

	def get_Nome(self):
		if self.Nome is None:
			return "Aguardando identificação..."
		else:
			try:
				return self.Nome.encode('utf-8')
			except:
				return self.Nome

	def get_DadosAlmoco(self):
		return json.dumps({'nome' : self.get_Nome(), 'valor': self.get_Valor(), 'peso': self.get_Peso(), 'tipo': self.TipoCliente, 'desconto': self.Desconto })

	def get_DadosLanche(self):
		prd = self.Produto
		if self.Produto is None:
			prd = "Selecione lanche ..."

		return json.dumps({'nome' : self.get_Nome(), 'produto': prd, 'quantidade': self.QntProduto, 'status': self.Status })

	def get_Confirma(self):
		# nada
		return ("confirma")

	def get_Cancela(self):
		self.resetaVariaveisOperacao()
		return ("cancela")

	def get_Suco(self):
		# nada
		return ("suco")

	def set_Suco(self, quantidade):
		self.Suco = quantidade
		return (str(quantidade))

		set_QuantidadeLanche

	def set_QntProduto(self, quantidade):
		self.QntProduto = quantidade
		return (str(quantidade))

	def set_Nome(self,nome):
		return self.set_Matricula(self.db.getMatrFromName(nome))

	def set_Produto(self, produto):
		self.Produto = produto
		return produto

	def set_DataEvento(self, dataevento=None):

		if dataevento is None:
			logging.info('Sem data do registro: assumindo hoje!')
			date = datetime.datetime.now()
			dataevento = "%02d/%02d/%04d" % (date.day, date.month, date.year)
		else:
			try:
				day, month, year = dataevento.split('/')
				datetime.datetime(int(year), int(month), int(day))

			except ValueError:
				logging.info("Data invalida. assumindo hoje! " +  str(dataevento))
				date = datetime.datetime.now()
				dataevento = "%02d/%02d/%04d" % (date.day, date.month, date.year)

		self.DataEvento = dataevento
		return dataevento

	def set_Matricula(self, matricula):

		logging.info("Recebida matricula: " +  str(matricula))

		self.Nome = self.db.getNameFromMatr(matricula)
		self.TipoCliente = self.db.getTypeClientFromMatr(matricula)

		if self.TipoCliente is not None:
			self.Desconto    = self.pegaDesconto(self.TipoCliente)

		logging.info("Setou nome: " + self.Nome)
		logging.info("Cliente: " + self.Nome + " matricula: " + str(matricula) + \
			         " TipoCliente: " + str(self.TipoCliente)      + " Desconto: "  + str(self.Desconto))
		return self.Nome


	def set_ConfirmaLanche(self, cliente, manter, produto = None, valor_almoco = None, quantidade = None):

		logging.info("Recebeu nome: " + cliente)

		if self.DataEvento is None:
			self.set_DataEvento()

		if cliente is not None and cliente != "nome":
			self.Nome = cliente

		if self.Nome is None:
			logging.info('Sem nome para registrar')
			return "Erro"
			
		if valor_almoco is not None:
			self.Produto     = 'Almoço'
			self.QntProduto  = 1

			if self.CadastraDadosLanche(valor_almoco):
				reg_almoco = True

			else: 
				logging.info('Nao registrou almoço!')
		else: 
			valor_almoco = 'não tem almoço'

		if produto is not None:
			self.Produto     = produto

		if quantidade is not None:
			self.QntProduto  = quantidade

		logging.info( "Dados a serem registrados:")
		logging.info( "Nome    : " + str(self.Nome))
		logging.info( "Produto : " + str(self.Produto))
		logging.info( "Quantid.: " + str(self.QntProduto))
		logging.info( "Valor   : " + str(valor_almoco))
	
		if self.CadastraDadosLanche():
			if manter != '1':
				self.Nome = None
			else:
				self.Status = "Registrado com sucesso!"
			self.resetaVariaveisOperacao(self.Nome)

		else:
			logging.info('Nao registrou!')

		return ({'nome': self.Nome, 'produto': None, 'quantidade': None})

	def set_BarCodeId(self, barcodeid):
		if barcodeid == "FALHA_LEITOR":
			logging.info("Erro no leitor de codigo de barras")
			return "Erro"

		self.idBarCode = barcodeid
		if self.idBarCode is not None:
			reactor.callLater(0.1,self.newBarCodeId)

		return (str(barcodeid))


	def CadastraDadosLanche(self, valor_total = None):
		try:
			# date = datetime.datetime.now()
			# timestamp = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)
			logging.info("Iniciando cadastro de consumo no dia: " + str(self.DataEvento))

			if self.Produto is not None:
				if valor_total is None and self.QntProduto is not None and int(self.QntProduto) > 0:
					valor_prd = float(self.db.getValueOfProduct(self.Produto))
					valor_total = "%.2f" % (valor_prd * int(self.QntProduto))

				if valor_total is not None and valor_total > 0 and int(self.QntProduto) > 0:
					self.db.cadastraEntradasRegistradas (self.Nome, self.Produto, self.QntProduto, valor_total, self.DataEvento)
		except Exception as e:
			logging.info("Erro no cadastro de consumo: " + str (e))

		return True

	def alteraEntradaRegistrada(self, id, campo):
		data = self.db.alteraEntradasRegistradas (id, campo,"SIM")
	
		if campo == "pago":
			json_data = json.loads(json.dumps(data))
			for table, value in json_data.items():
				for d in value:
					self.db.realizaDeposito(id, d['cliente'], d['datahora'], d['valor'])

			data = self.db.alteraEntradasRegistradas (id, "removido","fechado")

		return True

	def get_UltimaAtualizacao (self):
		if self.ultima_atualizacao is None:
			return "Nunca"

		return 	self.ultima_atualizacao

	

# Código de Barras
	def newBarCodeId(self):
		barCode = (int(self.idBarCode) - 10000000) / 10
		self.Nome = self.db.getNameFromMatr(barCode)
		logging.info("Cliente: " + self.Nome.encode('utf-8') + " matricula: " + str(barCode))


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

	sistema = IniciaSistema(enviroment)
	
	logging.info( "ControleLanche starting...")
	almoco = ProcLanchesCantina(sistema)

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print("KeyboardInterrupt")
		reactor.stop()

