#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import serial
import os, signal
import sys
from twisted.internet import reactor
from _serial import SerialModule

class BalanceFood():

	def __init__(self,port,baudrate,new_weight, logging = None):

		self.logging = logging

		self.baudrate = baudrate
		self.port = port
		self.rtscts = 0
		self.new_weight = new_weight

		self.rxbuffer = ""
		self.ser = None

		# self.fn_cbk_new_event = fn_cbk_new_event

		if self.port != 'AAAA':
			self.ser = SerialModule(self.port, self.baudrate, self.rtscts,
			self.__new_data_handler,
			self.__lost_connection_handler,
			self.__new_connection_handler)

	def setWeightEvent (self):
		if self.port == 'AAAA':
			self.new_weight('0.798')
			return
		else:
			if self.ser is not None and self.ser.dev is not None:
				self.ser.dev.writeSomeData("\x05")
				return
		
		self.new_weight('0')

	def __process_response(self,data):
		#print "Process_response"

		# printByte(data)

		try:
			gramas = float((int(data[5]) + int(data[4]) * 10 + int(data[3]) * 100)/float(1000))
			kilos  = int(data[2]) + int(data[1]) * 10 
			peso = float(kilos + gramas)

			self.new_weight(peso)

		except Exception, e:
			self.logging.info ("ERRO no processamento da balanca: " + str(e))
			self.logging.info (data)

	def __complete_reponse(self, data):
		message = None
		tam_pack = None

		try:
			if len(data) < 7: 
				message = "RESPONSE_INCOMPLETE"
				return message,tam_pack

			if (data[0] == '\x02' and data[6] == '\x03'): 
				message = "RESPONSE_COMPLETE"
				tam_pack = 7
				return message,tam_pack

		except Exception, e:
			self.logging.info ("ERRO no processamento da balanca: " + str(e))

		message = "ERROR_PACKAGE"
		return message,tam_pack

	def __new_data_handler(self, data):   
		self.rxbuffer += data

		reactor.callLater(0.001,self.__process_serial_data)

	def __process_serial_data(self):
		# Test all bytes arriveds
		message,tam_pack = self.__complete_reponse(self.rxbuffer)
		if message == "RESPONSE_INCOMPLETE":
			return

		elif message == "ERROR_PACKAGE":
			self.discard_transaction()
			return 

		self.__process_response(self.rxbuffer[:tam_pack])
		self.rxbuffer = self.rxbuffer[tam_pack:]

		reactor.callLater(0.001,self.__process_serial_data)

	def __clear_rxbuffer(self):
		self.rxbuffer = ""

	def discard_transaction(self):
		self.__clear_rxbuffer()

	def __lost_connection_handler(self):
		self.logging.info("Connection lost")
		self.ser = None
		reactor.callLater(2, self.__try_to_serial_connect)

	def __try_to_serial_connect(self):
		self.ser = None
		try:
			self.ser = SerialModule(self.port, self.baudrate, self.rtscts,
				self.__new_data_handler,
				self.__lost_connection_handler,
				self.__new_connection_handler)

		except Exception, e:
			reactor.callLater(5, self.__try_to_serial_connect)

	def __new_connection_handler(self):
		print "new connection"

def __new_weight(peso):
	print "Peso: " + str(peso)

if __name__ == '__main__':
#	try:
		if len(sys.argv) < 2:
			print "Try " + sys.argv[0] + " port baudrate"
			sys.exit(1)
		
		port = sys.argv[1]
		baudrate = sys.argv[2]

		balance = BalanceFood(port, baudrate, __new_weight)
		print "Waiting balance...."
		balance.setWeightEvent()

		reactor.run()

#	except Exception, e:
#		print "Erro main: "+str(e)


