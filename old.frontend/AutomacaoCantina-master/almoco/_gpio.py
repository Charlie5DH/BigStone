#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import RPi.GPIO as GPIO
from twisted.internet import reactor


class mngGPIO():
	def __init__(self):
		print "Initialied the mngGPIO module. GPIO in BCM mode"
		GPIO.cleanup()
		GPIO.setmode(GPIO.BCM)

	def setup_pin(self, pin, mode, pud_down = None):

		if   mode == "INPUT":  
			if   pud_down == "PULL_DOWN": resistor = GPIO.PUD_DOWN
			elif pud_down == "PULL_UP":   resistor = GPIO.PUD_UP

			GPIO.setup(pin, GPIO.IN, resistor)

		elif mode == "OUTPUT": 
			GPIO.setup(pin, GPIO.OUT)

	def read_pin(self, pin):
		return GPIO.input(pin)
		
	def register_pin_incallback(self, pin, event, callback):
		if event == "RISING":
			GPIO.add_event_detect(pin, GPIO.RISING)

		elif event == "FALLING":
			GPIO.add_event_detect(pin, GPIO.FALLING)
			
		elif event == "BOTH":
			GPIO.add_event_detect(pin, GPIO.BOTH)

		GPIO.add_event_callback(pin, callback)

	def io_set (self, pin):
		GPIO.output (pin,GPIO.HIGH)

	def io_reset (self, pin):
		GPIO.output (pin,GPIO.LOW)

if __name__ == '__main__':

	def callback_gpio(pin):
		print "Aconteceu evento no sensor.....", pin

	mnggpio = mngGPIO()
	mnggpio.setup_pin(4, "INPUT", "PULL_DOWN")
	mnggpio.register_pin_incallback(4, "BOTH", callback_gpio)

	reactor.run()
