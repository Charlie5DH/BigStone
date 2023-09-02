#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os, glob, stat
import datetime
import pwd
import MySQLdb


class dbData():
	def __init__(self, host, user, passwd, db, logging = None):
	
		self.logging = logging
		self.log ("dbData init")

		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
		self.lastID = 0

		self.connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, charset="utf8", use_unicode=True)

	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print(msg)

	def close(self):
		try:
			self.connection.close()
		except  Exception as e:
			self.log ( "Erro 02 ao fechar conexao com o banco: " + str(e))

	def exec_query(self, query):
		try:
			cursor = self.connection.cursor()
			cursor.execute(query)
			self.connection.commit()

			try:
				self.lastID = cursor.lastrowid
			except Exception as a:
				self.log ( "nao pegou ultimo id: " + str(a))
				self.lastID = 0

			result = cursor.fetchone()
			if result is not None:
				return result[0]

			return 0

		except Exception as e:
			self.log ( "Erro 01 na execucao da query: " + str(e))
			try:
				self.connection.rollback()

			except  Exception as er:
				self.log ( "Erro 03 de conexao com o banco: " + str(er))
		
		return None
		
	def select_to_json(self, query):

		try:
			#print "dbData: ", query
			cursor = self.connection.cursor( MySQLdb.cursors.DictCursor )
			cursor.execute(query)

			return cursor.fetchall()
		
		except Exception as e:
			self.log ( "Erro 04 na execucao da query: " + str(e))
			
		self.log("dbData::select_to_json: ", query)
		return None

	def select_to_csv(self, query):
		try:
			cursor = self.connection.cursor()
			cursor.execute(query)

			return cursor.fetchall()

		except Exception as e:
			self.log ( "Erro 05 na execucao da query: " + str(e))

		return None

	def getLastID(self):
		return self.lastID


