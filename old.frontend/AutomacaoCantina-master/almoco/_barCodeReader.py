#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, signal
import sys
from twisted.internet import reactor

hid = { 4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm', 17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y', 29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ', 45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';' , 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'  }

hid2 = { 4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M', 17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y', 29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ', 45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':' , 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'  }

class BarCodeReader ():

	def __init__(self,port,fb_function):

		print "BarCodeReader init!"
		self.port = port
		self.fb_function = fb_function
		self.tmr_getBarCode = None

		if self.port != 'AAAA':
			self.fdDevBarCode = open(self.port, "rb")

	def getIDFromBarCode (self):
		try:
			if self.port != 'AAAA':
				buffer = self.fdDevBarCode.read(8)
				
				for c in buffer:
					if ord(c) > 0:

						##  40 is carriage return which signifies
						##  we are done looking for characters
						if int(ord(c)) == 40:
							self.done = True
							break;

						##  If we are shifted then we have to 
						##  use the hid2 characters.
						if self.shift: 
				
							## If it is a '2' then it is the shift key
							if int(ord(c)) == 2 :
								self.shift = True
	
							## if not a 2 then lookup the mapping
							else:
								self.idBarCode += hid2[ int(ord(c)) ]
								self.shift = False
	
						##  If we are not shifted then use
	
						##  the hid characters
	
						else:
							## If it is a '2' then it is the shift key
							if int(ord(c)) == 2 :
								self.shift = True
	
							## if not a 2 then lookup the mapping
							else:
								self.idBarCode += hid[ int(ord(c)) ]

			if not self.done:
				if self.stop_trys:
					return 0

				reactor.callWhenRunning(self.getIDFromBarCode)
			
				if self.port == 'AAAA':
					self.done = True
					self.idBarCode = ID_TEST

				return (0)

			reactor.callLater(1,self.fb_function)

		except KeyboardInterrupt:
			self.fdDevBarCode.close()

		except Exception, e:
			print "Erro bar code: " + str(e)

		return 0

	def getBarCode (self):
		self.idBarCode = ""
		self.shift     = False
		self.done      = False
		self.stop_trys = False

		reactor.callLater(1,self.getIDFromBarCode)

def fb_function ():
	print "idBarCode: " + str(barcode.idBarCode)

ID_TEST = 1290
if __name__ == '__main__':
	try:
		if len(sys.argv) < 2:
			print "Try " + sys.argv[0] + " port_barcode"
			sys.exit(1)
		
		port_barcode = sys.argv[1]

		barcode = BarCodeReader(port_barcode,fb_function)
		barcode.getBarCode()

		reactor.run()

	except Exception, e:
		print "Erro main: "+str(e)


