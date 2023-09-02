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

PORT_HTTP = 4568
I = ""


class ProcRemoneIP():

	def __init__(self):

		self.base_data_path = os.path.dirname(os.path.abspath(__file__))
		self.load_settings()
		self.ip = None

		logging.info("Controlador de Regitros de Almoços da Cantina")

		signal.signal(signal.SIGINT, self.signal_handler)
		self.thr_http = reactor.callInThread(self.http_run)

	def log_init(self, log_path):
		log_format = '%(asctime)s:%(filename)s:%(lineno)4s - %(funcName)s(): %(message)s'

		a = logging.getLogger('')
		a.setLevel(logging.INFO)

		handler = logging.handlers.RotatingFileHandler("/".join((log_path,"getRemoteIP.log")), maxBytes=100000, backupCount=1000)
		handler.setLevel(logging.INFO)

		formatter = logging.Formatter(log_format)
		handler.setFormatter(formatter)

		a.addHandler(handler)

	def load_settings(self):

		log_path = os.path.join(self.base_data_path,"logs")

		if not os.path.isdir(log_path): 
			os.mkdir(log_path)

		self.log_init(log_path)


	def signal_handler(self, signal, frame):
		logging.info('You pressed Ctrl+C!')
		reactor.stop()
		sys.exit(0)

	def run(self):
		tempo_loop=0.5


		reactor.callLater(tempo_loop, self.run)

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

	def get_IP(self):
		if self.ip is None:
			return "Aguardando conexao sistema registros"
		else:
                    return str(self.ip) + ";" + str(self.date_alive)

	def set_IP(self, ip):
		self.ip = ip
		date = datetime.datetime.now()
		self.date_alive = "%02d/%02d/%04d %02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute)
		logging.info("Chegou endereco IP de um sistema remoto: " + self.ip)

# Process init
#

def SIGNAL_CustomEventHandler(num, frame):
	k={1:"SIGHUP", 2:"SIGINT", 9:"SIGKILL", 15:"SIGTERM"}

	logging.info( "Recieved signal " + str(num) + " - " + k[num])

	reactor.stop()
	os._exit(1)

if __name__ == '__main__':

	logging.info( "Remore ip starting...")
	remote_ip = ProcRemoneIP()

	try:
		signal.signal(signal.SIGINT, SIGNAL_CustomEventHandler)
		signal.signal(signal.SIGHUP, SIGNAL_CustomEventHandler)
		reactor.run()

	except KeyboardInterrupt:
		print "KeyboardInterrupt"
		reactor.stop()

