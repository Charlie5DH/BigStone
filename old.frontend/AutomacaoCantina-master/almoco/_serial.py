#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import asyncore, sys, serial
from sys import stdout

from twisted.internet.serialport import SerialPort
from twisted.internet import reactor

class SerialHandler(asyncore.dispatcher):

	def __init__(self, new_data_handler, lost_connection_handler, new_connection_handler):
		asyncore.dispatcher.__init__(self)
		self.new_data_handler = new_data_handler
		self.new_connection_handler = new_connection_handler
		self.lost_connection_handler = lost_connection_handler

	def makeConnection(self, data1):
		print "makeconnection"
		self.new_connection_handler()

	def connectionLost(self, reason):
		print "connectionLost"
		self.lost_connection_handler()

	def connectionMade(self):
		print 'Connection made!'
		self.tzero = time.time()

	def printByte(self, char_array):
		for TT in char_array:
			aux = "0x%02X" % ord(TT)
			stdout.write(aux + " ")
		stdout.write("\n")

	def dataReceived(self, data):
		self.new_data_handler(data)
		#for ii in data:
		#	self.printByte(ii)

class SerialModule():

	def __init__(self, port, baudrate, rtscts, new_data_handler, lost_connection_handler, new_connection_handler):
		sh = SerialHandler(new_data_handler, lost_connection_handler, new_connection_handler)

		bytesize=serial.EIGHTBITS
		parity=serial.PARITY_EVEN
		stopbits=serial.STOPBITS_ONE
		timeout=0
		xonxoff=0
		self.dev = None

		print "PORTA: ",  port, baudrate, rtscts, bytesize, parity, stopbits

		try:
			self.dev = SerialPort(sh, port, reactor, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts)
			self.dev.flushInput()
			self.dev.flushOutput()

		except Exception, e:
			print "Erro ao iniciar a serial: " + str(e)
			return None

	def start(self):
		reactor.run()

	

if __name__ == '__main__':			

	def new_data_handler(data):
		print "new_data_handler:" + data

	def lost_connection_handler():
		print "lost connection"

	def new_connection_handler():
		print "new_connection_handler"

	### SerialPort.protocol = SerialHandler()
	port='/dev/ttyUSB0'
	baudrate='115200'
	rtscts = 1
	sermod = SerialModule(port, baudrate, rtscts, 
				new_data_handler, 
				lost_connection_handler, 
				new_connection_handler)
	#sermod.dev.writeSomeData("\xBA\x03\x40\x01\xF8")
	sermod.dev.writeSomeData("\xBA\x02\x01\xB9")

	reactor.run()
	asyncore.loop()
