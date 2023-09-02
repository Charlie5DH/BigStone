#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import datetime

from sys import stdout

def printByte(char_array):
        stdout.write(str(datetime.datetime.now()) + " - ")
	for TT in char_array:
		aux = "0x%02X" % ord(TT)
		stdout.write(aux + " ")

	stdout.write("\n")

