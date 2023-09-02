#!/usr/bin/python
import sys
import json
import datetime
import signal,os
from shutil import copyfile
import time

from twisted.internet import reactor
import SimpleHTTPServer
import SocketServer
import socket
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.escape
import tornado.web
import logging
import time

# Locals imports
from _emailcli import *
from _monta_mensagem import *
from _server_http import *

# Global lib imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from process_data import *
from _config import *

#
# Trace
#
DIR_TRACE="trace/"
FILE_TRACE="trace_envio_email.log"

#
# HTTP Server
#

PORT_HTTP = 4569
I = ""

#
# Processamento das mensagens
# 

class DespachadorEmail():

	def __init__(self):
		self.base_data_path = os.path.dirname(os.path.abspath(__file__)) 
		self.log_init()
		logging.info ("Despachador de Emails da Cantina INIT")
		signal.signal(signal.SIGINT, self.signal_handler)
		self.thr_http = reactor.callInThread(self.http_run)

		self.db = ProcessaDados("production", logging)

		self.ConfEmail   = { 'email_server' : None, 'email_smtp_port' : None, 'email_from' : None, 'email_passwd' : None, 'email_to' : None, 'email_subject' : None, 'email_from_name' : None, 'email_cc' : None, 'email_bcc' : None }
		if self.pegaConfEmail() is False:
			print ("Erro na carga dos dados do servidor")
			logging.info ("Erro na carga dos dados do servidor")
			FinalizaSistema()

		self.eml_server = self.IniciaEmail()

		self.messages_exec = []

	def clients_init(self):
		try:
			if self.db is not None:
				self.db.close()
		except:
			pass
		self.db = ProcessaDados("production", logging)

		try:
			if self.eml_server is not None:
				self.eml_server.close()
		except:
			pass
		self.eml_server = self.IniciaEmail()

	def log_init(self):
		log_path = os.path.join(self.base_data_path,DIR_TRACE)

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.INFO)

		handler = logging.handlers.RotatingFileHandler("/".join((log_path,FILE_TRACE)), maxBytes=10000000, backupCount=1000)
		handler.setLevel(logging.INFO)

		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def signal_handler(self, signal, frame):
		logging.info('You pressed Ctrl+C!')
		FinalizaSistema()

	def run(self):
		tempo_loop=0.5
		reactor.callLater(tempo_loop, self.run)

	def inicia_despacho_email(self, envio_para, data_ini, destinatario):
		self.envio_para = envio_para

		if data_ini is None or len(data_ini) < 1:
			date = datetime.datetime.now()
			self.data_ini= "01/01/%04d" % (date.year)
		else:
			self.data_ini = data_ini
		self.destinatario = destinatario.encode('utf-8')

		logging.info("enviopara: " + self.envio_para)
		logging.info("dataini: " + self.data_ini)

		if len(self.destinatario) < 2:
			logging.info("destinatario: None")
			self.destinatario = None
		else:
			logging.info("destinatario: " + self.destinatario)
		
		reactor.callInThread(self.executa_despacho_email)

		return "Depacho iniciado"

	def executa_despacho_email(self):

		self.clients_init()

		logging.info("Despachador de mensagens de saldo para: " + self.envio_para)
		logging.info("data inicial: " + self.data_ini)

		self.ConfEmail['email_subject']   = 'Relatorio de consumo da Cantina'

		clientes = self.db.getInfoAllClients()

		contador = 0
		contador1 = 0
		contador2 = 0
		for cliente in clientes:
			contador += 1

			if cliente[0] is None:
				logging.info ("sem nome")
				continue
			nome = cliente[0].encode('utf-8')

			if self.destinatario is not None and self.destinatario != nome:
				# mandar para uma pessoa especifica
				continue
			
			if cliente[1] is None or len(cliente[1]) < 5:
				logging.info (cliente[0] + " sem email")
				continue

			email = cliente[1]			
			contador1 += 1

			if self.destinatario is None:
				tipo_cliente = self.db.getTypeClientFromName (nome)

				if self.envio_para == "Aluno" and tipo_cliente == "Professor":
					# NAO envia para professores
					logging.info( nome + " eh professor: nao envia" )
					continue
					
				if self.envio_para == "Professor" and tipo_cliente == "Aluno":
					# NAO envia para alunos
					logging.info( nome + " eh aluno: nao envia" )
					continue

				if self.envio_para == "Unico":
					continue

			logging.info ("Email para: " + email)
			creditos, debitos, contador, primeira_data, ultima_data, saldo_anterior, saldo_periodo, saldo_final =  self.db.getSaldoCliente(nome, self.data_ini)

			if contador == 0:
				logging.info ("Nao tem nada para mandar: cancela envio para " + email)
				continue

			contador2 += 1
			msg = { 'contador': contador2, 'nome': nome.decode('utf-8'), 'email': email, 'saldo': format(float(saldo_final),'0.2f') }
			logging.info (msg)
			self.messages_exec.append(msg)

			date = datetime.datetime.now()
			datahora_envio = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)

			msg = MontaEmailCliente(nome, email, logging)
			msg.MessageClient(self.db, saldo_anterior, saldo_final, self.data_ini, ultima_data)

			if TESTE:
				if email == "dariva@gmail.com":
					print("enviando.....")
					self.NotificaViaEmail (email, msg.message)
					
			else:
				if self.NotificaViaEmail (email, msg.message):
					self.db.setInfoEmailEnviado(nome, saldo_final, datahora_envio)
					time.sleep(2)

				else:
					logging.info ( "Nao enviada" )

		logging.info ( "Fim: " + str(contador) + " | " + str(contador1) + " | " + str(contador2))

	def get_running_messages (self):
		messages = self.messages_exec
		self.messages_exec = []

		return messages

	def mensagem_coletiva(self, arq_html):

		logging.info("Despachador de mensagem coletiva")

		self.ConfEmail['email_subject']   = 'Mensagem de boas vindas'

		clientes = self.db.getInfoAllClients()

		contador = 0
		contador1 = 0
		for cliente in clientes:

			contador += 1

			if cliente[0] is None:
				logging.info ("sem nome")
				continue
			
			if cliente[1] is None or len(cliente[1]) < 3:
				logging.info (cliente[0] + " sem email")
				continue
			
			contador1 += 1
			nome = cliente[0].encode('utf-8')
			email = cliente[1]

			date = datetime.datetime.now()
			datahora_envio = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)

			msg = MontaEmailCliente(nome, email, logging)

			msg.MessageColetiva(arq_html)

			logging.info ("Clientes: " + str(contador) + " Enviados: " + str(contador1))
			logging.info ("Enviando email para" + email + " | " + str(contador) + " : " + str(contador1))
			self.NotificaViaEmail (email, msg.message)

			time.sleep(1)

		logging.info ( "Fim" + str(contador) + " | " + str(contador1))

	def handle_request(self, request):
		message = "You requested %s\n" % request.uri
		request.write("HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s" % (len(message), message))
		request.finish()

	def http_run(self, port=PORT_HTTP):

		application = tornado.web.Application([
			(r"/(.*)", AppHandler, dict(obj=self)),
		])
		application.listen(PORT_HTTP)
		tornado.ioloop.IOLoop.instance().start()

		logging.info("Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT_HTTP))

	def stop(self):
		tornado.ioloop.IOLoop.instance().stop()

	def pegaConfEmail (self):

		email_cfg = self.base_data_path + "/email.cfg"

		if not os.path.isfile(email_cfg):
			logging.info ( "Nao tem configuracao de email")
			logging.info ( "Arquivo \"%s\" nao localizado! " % email_cfg)
			return False
		
		self.ini_sett = IniSett(email_cfg)
		try:
			self.ConfEmail['email_server']    = self.ini_sett.get('email','server')
			self.ConfEmail['email_smtp_port'] = self.ini_sett.get('email','smtp_port')
			self.ConfEmail['email_from']      = self.ini_sett.get('email','from')
			self.ConfEmail['email_from_name'] = self.ini_sett.get('email','from_name')
			self.ConfEmail['email_passwd']    = self.ini_sett.get('email','passwd')
			self.ConfEmail['email_bcc']       = self.ini_sett.get('email','bcc')
			#self.ConfEmail['email_subject']   = self.ini_sett.get('email','subject')

		except:
			logging.info ( "Erro na configuracao do email")
			self.ConfEmail['email_to']        = None
			return False

		return True

	def IniciaEmail (self):

		server    = self.ConfEmail['email_server']
		smtp_port = self.ConfEmail['email_smtp_port']
		fromaddr  = self.ConfEmail['email_from']
		from_name = self.ConfEmail['email_from_name']
		password  = self.ConfEmail['email_passwd']

		return EmailClient(server, smtp_port, fromaddr, password, from_name, logging)

	def FinalizaEmail (self):
		self.eml_server.close()

	def NotificaViaEmail (self, toaddr, msg):

		if TESTE:
			if toaddr != "dariva@gmail.com":
				return False

		if self.eml_server is not None:
			ccaddr    = self.ConfEmail['email_cc']
			bccaddr   = self.ConfEmail['email_bcc']
			subject   = self.ConfEmail['email_subject']

			c = self.eml_server.emailsend (toaddr, subject, msg, ccaddr, bccaddr)

			if c:
				logging.info ( "E-mail enviado com sucesso para %s" % toaddr )
				return True

			else:
				logging.info ( "Erro! E-mail falhou")

		else:
			logging.info ( "Erro na inicializacao do servidor" )

		return False


	def FinalizaConexao (self):
		if self.Conn is not None:
			self.Conn.finalizaConexao()
			self.Conn = None

#
# Inicio do Processo
# 
def FinalizaSistema ():
	reactor.stop()
	os._exit(1)
	sys.exit(0)


def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	print("Recieved signal " + str(num) + " - " + k[num])

	FinalizaSistema()

if __name__ == '__main__':

	tipo = ""
	envio_para = "Todos"
	data_ini = None
	destinatario = None

	TESTE = False

	try:
		if len(sys.argv) >= 4:
			tipo = sys.argv[1]
			envio_para = sys.argv[2]
			data_ini = sys.argv[3]
			if envio_para == "Unico":
				if len(sys.argv[4]) < 3:
					print("Faltou o nome da pessoa a enviar")
				else:
					destinatario = sys.argv[4]

		else:
			print("Digite: " + sys.argv[0] + " [tipo] ....")
			print("Onde: tipo: ")
			print(" tipo == aviso")
			print(" tipo == cobranca <Aluno|Professor|Todos|Unico> <data_ini> [nome, se Unico]")
			
# ./motor_envia_email.py "cobranca" "Aluno" "08/03/2019"
# ./motor_envia_email.py "cobranca" "Professor" "08/03/2019"
# ./motor_envia_email.py "cobranca" "Todos" "08/03/2019"
# ./motor_envia_email.py "cobranca" "Unico" "08/03/2019" "ACALU SERENO MACHADO DA SILVA"

	except Exception as e:
		print ("Erro: " + str(e))

	print("Despachador de Emails da Cantina iniciando...")
	desp = DespachadorEmail()

	if tipo == "aviso":
		desp.mensagem_coletiva("Oficio_Inicio_Ano.html")

	elif tipo == "cobranca":
		desp.inicia_despacho_email(envio_para, data_ini, destinatario)

	else:
		print("Nao sei o tipo " + str(tipo))

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print("KeyboardInterrupt")
		reactor.stop()

