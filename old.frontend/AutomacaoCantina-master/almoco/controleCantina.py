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
from _barCodeReader import *
from _balanceFood import *
from _sendMyIP import *
from _syncDataServer import *

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from process_data import *

PORT_HTTP = 4567
I = ""

class IniciaSistema():

	def __init__(self, enviroment):

		self.file_log = ''
		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()

		print "log em: " + self.file_log

		logging.info("Controlador de Regitros de Almoços da Cantina")


		self.db = ProcessaDados(enviroment, logging)

		print "interface: ", interface

		self.sendIP = SendMyIP(URL_SERVER, interface, logging)
		
		self.syncDataServer = SyncDataServer(URL_SERVER, logging)

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

		self.file_log = "/".join((log_path,"controleCantina.log"))

		handler = logging.handlers.RotatingFileHandler(self.file_log, maxBytes=1000000, backupCount=1000)
		handler.setLevel(logging.DEBUG)

		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def run(self):
		tempo_loop=10
		if self.Sucesso > 10 :
			if self.sendIP.sendIP_toServer():
				self.Sucesso = 0
		else:
			self.Sucesso = self.Sucesso + 1

		reactor.callLater(tempo_loop, self.run)

	def sincronizaBaseDados(self):

		clientes = self.syncDataServer.getData('Clientes')

		if clientes is not None:
			logging.info("Atualizando tabela de Clientes")
			print clientes
			for table, value in clientes.items():
				if table == "Clientes" and value is not None:
 					self.db.processa_tabela(table,value)

		produtos = self.syncDataServer.getData('Produtos')

		if produtos is not None:
			logging.info("Atualizando tabela de Produtos")
			for table, value in produtos.items():
				if table == 'Produtos' and value is not None:
 					self.db.processa_tabela(table,value)


class ProcAlmocoCantina():

	def __init__(self, system, interface, port_balance, baudrate):

		self.db = system.db
		self.syncDataServer = system.syncDataServer

		signal.signal(signal.SIGINT, self.signal_handler)
		self.thr_http = reactor.callInThread(self.http_run)

		self.balance = BalanceFood(port_balance, baudrate ,self.__new_weight, logging)
		reactor.callLater(0.1,self.OperationBalance)

#		self.barcode = BarCodeReader(PORT_BARCODE, self.__new_barcode)
#		reactor.callLater(0.1,self.OperationBarCode)

		self.resetaVariaveisOperacao()

		self.pegaValoresProdutos()
		self.ultima_atualizacao = None


	def resetaVariaveisOperacao (self):
		self.conta_tout_balanca = 0
		self.Peso        = None
		self.Valor       = None
		self.TipoCliente = None
		self.Desconto    = None
		self.Produto     = None
		self.QntProduto  = 1

		self.idBarCode = None
		self.Nome      = None

		self.Suco      = None
		self.Confirma  = None
		self.Cancela   = None
		self.tmr_getWeight  = None
		self.tmr_getBarCode = None
		self.resetou = True

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
		tempo_loop=1
		if self.Sucesso > 10 :
			if self.sendIP.sendIP_toServer():
				self.Sucesso = 0

			self.pegaValoresProdutos()

		else:
			self.Sucesso = self.Sucesso + 1

		reactor.callLater(tempo_loop, self.run)

	def pegaValoresProdutos(self):
		valor_kg = float(self.db.getValueOfProduct("Almoco"))
		if valor_kg is not None:
			self.valor_kg_cadastrado = valor_kg

		valor_suco = float(self.db.getValueOfProduct("Suco"))
		if valor_suco is not None:
			self.valor_suco_cadastrado = valor_suco

	def pegaDesconto(self, tipo_cliente):
		desconto = float(self.db.getDiscontoOfClientType(tipo_cliente))
		if desconto is not None:
			return desconto
			
		return 0

	def get_NowOperation(self):
		# nada
		return ("now_operation")

	def get_Peso(self):
		if self.Peso is None:
			return "Aguardando balança..."
		else:
			return str(self.Peso)

	def get_Valor(self):
		if self.Valor is None:
			return "Aguardando balança..."
		else:
			return str(self.Valor)

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

		return json.dumps({'nome' : self.get_Nome(), 'produto': prd, 'quantidade': self.QntProduto })

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

	def set_Matricula(self, matricula):

		self.Nome = self.db.getNameFromMatr(matricula)
		self.TipoCliente = self.db.getTypeClientFromMatr(matricula)

		if self.TipoCliente is not None:
			self.Desconto    = self.pegaDesconto(self.TipoCliente)

		logging.info("Setou nome: " + self.Nome)
		logging.info("Cliente: " + self.Nome + " matricula: " + str(matricula) + \
			         " TipoCliente: " + self.TipoCliente      + " Desconto: "  + str(self.Desconto))
		return self.Nome

	def set_Confirma(self, cliente):

		logging.info("Recebeu nome: " + cliente)
		if cliente is not None and cliente != "nome":
			self.Nome = cliente

		if self.Nome is None:
			logging.info('Sem nome para registrar')
			return "Erro"

		logging.info( "Dados a serem registrados:")
		logging.info( "Nome    : " + str(self.Nome))
		logging.info( "Peso    : " + str(self.Peso))
		logging.info( "Valor   : " + str(self.Valor))
		logging.info( "Suco    : " + str(self.Suco))
		logging.info( "TipoClin: " + str(self.TipoCliente))
		logging.info( "Desconto: " + str(self.Desconto))

		if self.CadastraDadosAlmoco():
			self.resetaVariaveisOperacao()

		else:
			logging.info('Nao registrou!')

		return ("confirma")

	
	def set_ConfirmaLanche(self, cliente):

		logging.info("Recebeu nome: " + cliente)
		if cliente is not None and cliente != "nome":
			self.Nome = cliente

		if self.Nome is None:
			logging.info('Sem nome para registrar')
			return "Erro"

		logging.info( "Dados a serem registrados:")
		logging.info( "Nome    : " + str(self.Nome))
		logging.info( "Produto : " + str(self.Produto))
		logging.info( "Quantid.: " + str(self.QntProduto))
	
		if self.CadastraDadosLanche():
			self.resetaVariaveisOperacao()

		else:
			logging.info('Nao registrou!')

		return ("confirma")

	def set_BarCodeId(self, barcodeid):
		if barcodeid == "FALHA_LEITOR":
			logging.info("Erro no leitor de codigo de barras")
			return "Erro"

		self.idBarCode = barcodeid
		if self.idBarCode is not None:
			reactor.callLater(0.1,self.newBarCodeId)

		return (str(barcodeid))


	def CadastraDadosAlmoco(self):
		
		date = datetime.datetime.now()
		timestamp = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)
		logging.info("Iniciando cadastro de almoco")

		if self.Valor is not None:
			valor = self.Valor 
			if self.Desconto is not None and float(self.Desconto) > 0:
				d = 1 - float(float(self.Desconto)/100)
				valor = float(self.Valor) * d

			data = self.db.cadastraEntradasRegistradas (self.Nome, "Almoco", self.Peso, str(valor), timestamp)
		#	if data is not None:
		#		self.syncDataServer.setData('EntradasRegistradas', data)

		if self.Suco is not None:
			valor_suco = "%.2f" % (self.valor_suco_cadastrado * self.Suco)
			data = self.db.cadastraEntradasRegistradas (self.Nome, "Suco", self.Suco, valor_suco, timestamp)
		#	if data is not None:
		#		self.syncDataServer.setData('EntradasRegistradas', data)
		return True

	def CadastraDadosLanche(self):
		
		date = datetime.datetime.now()
		timestamp = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)
		logging.info("Iniciando cadastro de lanche")

		if self.Produto is not None:
			valor_prd = float(self.db.getValueOfProduct(self.Produto))
			valor_total = "%.2f" % (valor_prd * self.QntProduto)
			data = self.db.cadastraEntradasRegistradas (self.Nome, self.Produto, self.QntProduto, valor_total, timestamp)
		#	if data is not None:
		#		self.syncDataServer.setData('EntradasRegistradas', data)

		return True

	def alteraEntradaRegistrada(self, id, campo):
		data = self.db.alteraEntradasRegistradas (id, campo,"SIM")
	
		if campo == "pago":
			json_data = json.loads(json.dumps(data))
			for table, value in json_data.items():
				for d in value:
					self.db.realizaDeposito(id, d['cliente'], d['datahora'], d['valor'])

			data = self.db.alteraEntradasRegistradas (id, "removido","fechado")

		# if data is not None:
		# 	self.syncDataServer.setData('EntradasRegistradas', data)

		# 	logging.info("EntradaRegistrada (" + str(id) + ") campo \'" + str(campo) + "\' alterada com sucesso")
		# 	return True

		# return False

		return True

	def get_UltimaAtualizacao (self):
		if self.ultima_atualizacao is None:
			return "Nunca"

		return 	self.ultima_atualizacao

	def sincronizaEntradasRegistradas(self, dia):

		if dia is not None:
			data = self.db.getEntradasRegistradas(dia)

			try:
				logging.info("Sincronizando EntradasRegistradas do dia " + str(dia))
				self.syncDataServer.setData('EntradasRegistradas', data)

				date = datetime.datetime.now()
				timestamp = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)
				self.ultima_atualizacao = timestamp
				
				return True

			except Except as e:
				logging.info("Erro na sinc das EntradasRegistradas do dia " + str(dia) + " erro: " + str (e))
				return False

		logging.info("Erro na sinc das EntradasRegistradas do dia " + str(dia) + " dia invalido")
		return False
		

# Código de Barras
	def newBarCodeId(self):
		if int(self.idBarCode) < 20000000:
			barCode = (int(self.idBarCode) - 10000000) / 10
		else:
			barCode = (int(self.idBarCode)) / 10

		self.Nome = self.set_Matricula(str(barCode))
		logging.info("Cliente: " + self.Nome.encode('utf-8') + " matricula: " + str(barCode))

# balanca
	def OperationBalance(self):
		self.tmr_getWeight = reactor.callLater(1, self.timeOutWaitingBalanceReturn)
		self.balance.setWeightEvent()

	def __new_weight(self,peso):
		self.Peso = float(peso)

		# logging.info( "Done balance: " + str(self.Peso))

		if self.Peso is not None:
			self.Valor = "%.2f" % (self.valor_kg_cadastrado * self.Peso)

		if self.tmr_getWeight is not None:
			#logging.info( "Stop time out balance")
			self.tmr_getWeight.cancel()
			self.tmr_getWeight = None
			self.conta_tout_balanca = 0

			if self.resetou is True:
				self.resetaVariaveisOperacao()
				self.resetou = False
				reactor.callWhenRunning(self.OperationBalance)
			else:
				reactor.callLater(0.5,self.OperationBalance)

	def timeOutWaitingBalanceReturn (self):

		self.conta_tout_balanca = self.conta_tout_balanca + 1
		logging.info( "TimeOut Balanca: " + str(self.conta_tout_balanca))

		if self.conta_tout_balanca >=2:
			self.Peso  = None
			self.Valor = None
			self.conta_tout_balanca = 0

		reactor.callLater(0.5,self.OperationBalance)

#
# Process init
#

def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	logging.info( "Recieved signal " + str(num) + " - " + k[num])

	reactor.stop()
	os._exit(1)

if __name__ == '__main__':

	# Balance
	PORT_BALANCE="/dev/ttyUSB0"
	BAUDRATE="9600"

	# Bar Code
	PORT_BARCODE="/dev/hidraw0"

	# Interface de comunicacao com o front
	interface = "eth0"

	# Cadastro dos registros
	URL_SERVER = "http://54.207.127.233"

	# Ambiente
	enviroment = 'production'
	
	DEBUG = False
	if len(sys.argv) > 1:
		DEBUG = sys.argv[2]
		interface = sys.argv[1]
	
	if DEBUG:
		print "Modo DEBUG"

		# Balance
		PORT_BALANCE="AAAA"
		BAUDRATE="9600"

		# Bar Code
		PORT_BARCODE="AAAA"

		#URL_SERVER = "http://localhost"

		enviroment = 'development'

	sistema = IniciaSistema(enviroment)
	sistema.run()
	sistema.sincronizaBaseDados()
	
	logging.info( "ControleCantina starting...")
	almoco = ProcAlmocoCantina(sistema, interface, PORT_BALANCE, BAUDRATE)

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print "KeyboardInterrupt"
		reactor.stop()

