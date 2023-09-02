#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests

import netifaces
import signal, os
import datetime, time
import sys


PORT_HTTP = 4568
URI="/ip"


class SendMyIP():

	def __init__(self, url, interface, logging = None):

		self.logging = logging
		self.log ("Send my IP")
		self.ip = None
		self.interface = interface
		self.url_server = url + ":" + str(PORT_HTTP) + URI

		self.log("URL:" + self.url_server)
		self.sendIP_toServer()

	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print msg


	def sendIP_toServer(self):

		self.getIP_fromLocal ()

		if self.ip is None:
			self.log ("Erro ip")
			return False

		try:
			headers = {'Content-type':'application/x-www-form-urlencoded','Accept':'text/plain'}

			data_code = "ip_address=" + str(self.ip)
			self.log ( self.url_server)
			self.log ( data_code)
			r = requests.post(self.url_server, data=data_code, headers=headers, timeout=30)

			if r.status_code == 200 or  r.status_code == 201:
				self.log ( "Sucesso!")
				return True
			else:
				self.log ( r.status_code)

		except:
			self.log ( "Falha de conexao com server da cantina! Nao mandou codigo de barras.")
			
		return False

	def getIP_fromLocal (self):
		try:
			iface = netifaces.ifaddresses(self.interface).get(netifaces.AF_INET)

		except:
			self.log ( "Erro ao pegar a interface: " + str(self.interface))
			iface = None

		if iface != None:
			for j in iface:
				self.ip = j['addr']
			self.log ( "Encontrei ip: " + self.ip + " em " + self.interface)

	def getURLServer(self):
		return URL


#
# Process init
#

if __name__ == '__main__':

	print "Pega endereco IP e envia para servidor remoto"
	IP = SendMyIP("eth0")

