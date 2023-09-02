#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, glob, stat
import datetime
import pwd

class GeradorLog():
	def __init__(self,directory, filename, maxfiles, maxbytes, fn_cbk_rotate, no_ext):
		self.fn_cbk_rotate = fn_cbk_rotate
		self.maxbytes = maxbytes
		self.maxfiles = maxfiles

		if not os.path.exists(directory):
			print "Diretorio %s nao exist. Criando" % directory
			os.mkdir(directory)
			os.chown(directory,pwd.getpwnam('pi').pw_uid,pwd.getpwnam('pi').pw_uid)

		self.filename = directory + filename
		self.writed_bytes = 0
		self.noext = no_ext

		self.number_of_files = len(glob.glob(self.filename + ".*"))

		if self.noext is True:
			self.create_file()
		else:
			self.create_file_no_ext()

	def create_file_no_ext(self):

		# Excedeu o numero de arquivos
		if self.number_of_files >= self.maxfiles: self.number_of_files = 0

		if os.path.isfile (self.filename) is True:
			os.rename (self.filename, self.filename + "." + str(self.number_of_files + 1))

			# Update number of files in dir
			self.number_of_files = self.number_of_files + 1

		print "create no-ext: ", self.filename + "." + str (self.number_of_files)

		self.fd = os.open(self.filename, os.O_CREAT | os.O_WRONLY)


	def create_file(self):

		fname = self.filename + "." + str(self.number_of_files + 1)

		# Update number of files in dir
		self.number_of_files = self.number_of_files + 1

		print "create: ", self.filename + "." + str (self.number_of_files)

		self.fd = os.open(fname, os.O_CREAT | os.O_WRONLY)


	def close_file(self):
		os.close(self.fd)

	
	def trc(self, data, fmt = None):
		size_try_data = len(data)

		if (self.writed_bytes + size_try_data) > self.maxbytes:
			self.writed_bytes = 0

			self.close_file()

			if self.noext is True:
				self.create_file()
			else:
				self.create_file_no_ext()
	
			# The callback of application
			if self.fn_cbk_rotate is not None: self.fn_cbk_rotate()

		os.write(self.fd,str(datetime.datetime.now()) + " - ")
		if fmt == "HEX":
			for TT in data:
				aux = "0x%02X" % ord(TT)
				os.write(self.fd,aux + " ")

			os.write(self.fd,"\n")
		else:
			os.write(self.fd, data + "\r\n")

		self.writed_bytes = self.writed_bytes + size_try_data

	
	def reg(self, data):
                if data == '': return

		size_try_data = len(data)

		if (self.writed_bytes + size_try_data) > self.maxbytes:
			self.writed_bytes = 0

			self.close_file()

			if self.noext is True:
				self.create_file()
			else:
				self.create_file_no_ext()
	
			# The callback of application
			if self.fn_cbk_rotate is not None: self.fn_cbk_rotate()

		self.writed_bytes = self.writed_bytes + size_try_data
		os.write(self.fd, data + "\r\n")
		
	
	def virada_via_sinal_externo(self):

		self.writed_bytes = 0

		self.close_file()

		if self.noext is True:
			self.create_file()
		else:
			self.create_file_no_ext()
	
