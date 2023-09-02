
#!/usr/bin/python

import logging
import pwd
import grp
import datetime
import sys
import os, sys, glob
import struct
from db_data import *
import json
import time
from random import randint

class ProcessaDados ():

	DATABASE_NAME  = "cantina1_cantinadodindo";
	HOST_DB			= "localhost";
	USER_DB			= "root";
	PASSWD_DB		= "dariva12";

	CONFIG_TABLE_NAME       = "Configuracao";      
	CONFIG_COLUMN_ID        = "config_id";                
	CONFIG_COLUMN_INFO      = "config_info";              
	CONFIG_COLUMN_VALUE     = "config_value";             
	CONFIG_SERVER_IP        = "config_server_ip";         
	CONFIG_SERVER_USER      = "config_server_user";       
	CONFIG_SERVER_PASSWD    = "config_server_senha";      
	
	BALANCE_TABLE_NAME         = "Saldo_Cliente";      
	BALANCE_ID                 = "balance_id";                
	BALANCE_REAL               = "balance_saldo_cliente";   
	BALANCE_REAL_DATE          = "balance_update";           
	BALANCE_INITIAL            = "balance_inicial";  
	BALANCE_INITIAL_START_DATE = "balance_inicial_ini_data";
	BALANCE_INITIAL_END_DATE   = "balance_inicial_fim_data";
	BALANCE_NAME               = "balance_nome_cliente";         
	BALANCE_MATRICULA          = "balance_matricula"; 
															
	INPUT_TABLE_NAME        = "Entradas_Registradas";                   
	INPUT_COLUMN_ID         = "id"; 
	INPUT_COLUMN_ID_ORG     = "id_org";                         
	INPUT_COLUMN_OPERADOR   = "operador";                   
	INPUT_COLUMN_CLIENTE    = "cliente";                    
	INPUT_COLUMN_PRODUTO    = "produto";                    
	INPUT_COLUMN_VALOR      = "valor";                      
	INPUT_COLUMN_DATAHORA   = "datahora";                   
	INPUT_COLUMN_PAGO       = "pago";                       
	INPUT_COLUMN_REMOVIDO   = "removido";                   
	INPUT_COLUMN_QUANTIDADE = "quantidade";                 
															 
	PRODUCTS_TABLE_NAME     = "Produtos";            
	PRODUCTS_COLUMM_ID      = "prd_id";                     
	PRODUCTS_COLUMM_PRODUTO = "prd_produto";                
	PRODUCTS_COLUMM_VALOR   = "prd_valor";                  
															
	CLIENTS_TABLE_NAME        = "Clientes";            
	CLIENTS_COLUMM_ID         = "cliente_id";                 
	CLIENTS_COLUMM_NOME       = "cliente_nome";               
	CLIENTS_COLUMM_FAMILIA    = "cliente_familia";            
	CLIENTS_COLUMM_TIPO       = "cliente_tipo";               
	CLIENTS_COLUMM_DATA       = "cliente_data";               
	CLIENTS_COLUMM_ANO        = "cliente_ano";               
	CLIENTS_COLUMM_MATRICULA  = "cliente_matricula";               
	CLIENTS_COLUMM_PAIS_1     = "cliente_pais_1";            
	CLIENTS_COLUMM_PAIS_2     = "cliente_pais_2";            
	CLIENTS_COLUMM_EMAIL_1    = "cliente_email_1";            
	CLIENTS_COLUMM_EMAIL_2    = "cliente_email_2";            
	CLIENTS_COLUMM_TELEFONE_1 = "cliente_telefone_1";            
	CLIENTS_COLUMM_TELEFONE_2 = "cliente_telefone_2";            
	CLIENTS_COLUMM_TELEFONE_3 = "cliente_telefone_3";            
	CLIENTS_COLUMM_TELEFONE_4 = "cliente_telefone_4";            
	CLIENTS_COLUMM_TELEFONE_5 = "cliente_telefone_5";            
	CLIENTS_COLUMM_TELEFONE_6 = "cliente_telefone_6";            
	CLIENTS_COLUMM_TELEFONE_7 = "cliente_telefone_7";            
	CLIENTS_COLUMM_TELEFONE_8 = "cliente_telefone_8";            
	CLIENTS_COLUMM_TELEFONE_9 = "cliente_telefone_9";            
															
	TYPE_CLIENTS_TABLE_NAME      = "Tipo_Clientes";   
	TYPE_CLIENTS_COLUMM_ID       = "tipo_cliente_id";        
	TYPE_CLIENTS_COLUMM_TIPO     = "tipo_cliente_nome";      
	TYPE_CLIENTS_COLUMM_DESCONTO = "tipo_cliente_desconto"; 

	def __init__(self, enviroment = 'production', logging = None):
		self.logging = logging
		self.db = dbData (self.HOST_DB, self.USER_DB, self.PASSWD_DB, self.DATABASE_NAME)

		self.enviroment = enviroment

		self.log ( "ProcessaDados iniciado. Rodando na maquina: " + str(self.enviroment))

	def isProduction(self):
		if self.enviroment == 'production':
			return True

		return False

	def close (self):
		self.db.close()

	def db_reinit (self, msg=None):
		if msg is None:
			self.log ( "ERRO!!! Banco sendo reiniciado!!!")
		else:
			self.log ( msg)
			
		self.db.close()
		self.db = dbData (self.HOST_DB, self.USER_DB, self.PASSWD_DB, self.DATABASE_NAME)

	def exec_query(self, query, operation=None):
		resdb = None
		if query is not None:
			self.log("exec_query:: operation: " + str(operation) + " Query" + query)

			if operation is None:
				resdb = self.db.exec_query(query)

			elif operation == 'csv':
			 	resdb = self.db.select_to_csv(query)

			elif operation == 'json':
			 	resdb = self.db.select_to_json(query)

			if resdb is None:
				self.log("Erro: sem retorno do BD. Resetando....")
				self.db_reinit ()

		return resdb

	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print(msg)

	def CreateTable(self):
		self.CreateConfigTableName()
		self.CreateContactsTableName()
		self.CreateProductTableName()
		self.CreateClientTableName()
		self.CreateTypeClientTableName()

	def CreateConfigTableName (self):
		self.log ( "CreateConfigTableName " + self.CONFIG_TABLE_NAME)

		self.exec_query(
			"create table " +
			self.CONFIG_TABLE_NAME     + " (" +
			self.CONFIG_COLUMN_ID      + " integer primary key AUTO_INCREMENT, " +
			self.CONFIG_COLUMN_INFO    + " text, " +
			self.CONFIG_COLUMN_VALUE   + " text)")

	def CreateBalanceTable (self):
		self.log ( "CreateBalanceTable " + self.CONFIG_TABLE_NAME)

		self.exec_query(
			"create table " +
			self.BALANCE_TABLE_NAME         + " (" +
			self.BALANCE_ID                 + " integer primary key AUTO_INCREMENT, " +
			self.BALANCE_REAL               + " text, " +
			self.BALANCE_REAL_DATE          + " text, " +
			self.BALANCE_INITIAL            + " text, " +
			self.BALANCE_INITIAL_START_DATE + " text, " +
			self.BALANCE_INITIAL_END_DATE   + " text, " +
			self.BALANCE_NAME               + " text, " +
			self.BALANCE_MATRICULA          + " text)")

	def CreateInputTableName (self):
		self.log ( "CreateInputTableName " + self.INPUT_TABLE_NAME)

		self.exec_query(
				"create table " +
						self.INPUT_TABLE_NAME + " (" +
						self.INPUT_COLUMN_ID + " integer primary key AUTO_INCREMENT, " +
						self.INPUT_COLUMN_ID_ORG + " text, " +
						self.INPUT_COLUMN_OPERADOR + " text, " +
						self.INPUT_COLUMN_CLIENTE + " text, " +
						self.INPUT_COLUMN_PRODUTO + " text, " +
						self.INPUT_COLUMN_VALOR + " text, " +
						self.INPUT_COLUMN_DATAHORA + " text, " +
						self.INPUT_COLUMN_PAGO + " text, " +
						self.INPUT_COLUMN_REMOVIDO + " text, " +
						self.INPUT_COLUMN_QUANTIDADE + " text)")


	def CreateProductTableName (self):
		self.log ( "CreateProductTableName " + self.PRODUCTS_TABLE_NAME)

		self.exec_query(
				"create table " +
						self.PRODUCTS_TABLE_NAME + " (" +
						self.PRODUCTS_COLUMM_ID + " integer primary key AUTO_INCREMENT, " +
						self.PRODUCTS_COLUMM_PRODUTO + " text, " +
						self.PRODUCTS_COLUMM_VALOR + " text)")

	def CreateClientTableName (self):
		self.log ( "CreateClientTableName " + self.CLIENTS_TABLE_NAME)

		self.exec_query(
				"create table " +
						self.CLIENTS_TABLE_NAME        + " (" +
						self.CLIENTS_COLUMM_ID         + " integer primary key AUTO_INCREMENT, " +
						self.CLIENTS_COLUMM_NOME       + " text, " +
						self.CLIENTS_COLUMM_FAMILIA    + " text, " +
						self.CLIENTS_COLUMM_TIPO       + " text, " +
						self.CLIENTS_COLUMM_DATA       + " text, " +
						self.CLIENTS_COLUMM_ANO        + " text, " +
						self.CLIENTS_COLUMM_MATRICULA  + " text, " +
						self.CLIENTS_COLUMM_PAIS_1     + " text, " +
						self.CLIENTS_COLUMM_PAIS_2     + " text, " +
						self.CLIENTS_COLUMM_EMAIL_1    + " text, " +
						self.CLIENTS_COLUMM_EMAIL_2    + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_1 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_2 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_3 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_4 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_5 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_6 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_7 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_8 + " text, " +
						self.CLIENTS_COLUMM_TELEFONE_9 + " text)")

	def CreateTypeClientTableName (self):
		self.log ( "CreateTypeClientTableName " + self.TYPE_CLIENTS_TABLE_NAME)

		self.exec_query(
				"create table " +
						self.TYPE_CLIENTS_TABLE_NAME + " (" +
						self.TYPE_CLIENTS_COLUMM_ID + " integer primary key AUTO_INCREMENT, " +
						self.TYPE_CLIENTS_COLUMM_TIPO + " text, " +
						self.TYPE_CLIENTS_COLUMM_DESCONTO + " text)")

	def DropAllDB (self):
		self.dropDBConfig()
		self.dropDBEntradasRegistradas()
		self.dropDBProducts()
		self.dropDBClients()
		self.dropDBTypeClients()

	def dropDBConfig (self):
		self.exec_query("DROP TABLE IF EXISTS " + self.CONFIG_TABLE_NAME )

		self.CreateConfigTableName()


	def dropDBBalance (self):
		self.exec_query("DROP TABLE IF EXISTS " + self.BALANCE_TABLE_NAME )

		self.CreateBalanceTable()

	def dropDBEntradasRegistradas (self):
		self.exec_query("DROP TABLE IF EXISTS " + self.INPUT_TABLE_NAME )

		self.CreateInputTableName()

	def dropDBProducts (self):
		self.exec_query("DROP TABLE IF EXISTS " + self.PRODUCTS_TABLE_NAME )

		self.CreateProductTableName()

	def dropDBClients (self):
		self.log ( "Apagando tabela Clientes")
		self.exec_query("DROP TABLE IF EXISTS " + self.CLIENTS_TABLE_NAME )

		self.CreateClientTableName()

	def dropDBTypeClients (self):
		self.exec_query("DROP TABLE IF EXISTS " + self.TYPE_CLIENTS_TABLE_NAME )

		self.CreateTypeClientTableName()

	def processa_tabela(self, table, value):
		if table == self.TYPE_CLIENTS_TABLE_NAME:
			self.dropDBTypeClients()
			self.processa_tabela_tipo_cliente(value)

		elif table == self.CLIENTS_TABLE_NAME:
			#if self.isProduction() is False:
			#	self.dropDBClients()

			self.processa_tabela_cliente(value)

		elif table == self.PRODUCTS_TABLE_NAME:
			self.dropDBProducts()
			self.processa_tabela_produtos(value)

		elif table == self.INPUT_TABLE_NAME:
			# self.dropDBEntradasRegistradas()
			self.processa_tabela_entradas(value)

		elif table == self.CONFIG_TABLE_NAME:
			self.dropDBConfig()
			self.processa_tabela_config(value)

		else:
			self.log ( "ERRO: Tabela desconhecida: " + table)

	def processa_tabela_tipo_cliente(self, value):
		query = """
	   		INSERT INTO `""" + self.TYPE_CLIENTS_TABLE_NAME + """` (
		`""" + self.TYPE_CLIENTS_COLUMM_ID + """`,
		`""" + self.TYPE_CLIENTS_COLUMM_TIPO + """`,
		`""" + self.TYPE_CLIENTS_COLUMM_DESCONTO + """`
		) VALUES """

		i=0
		for s in value:
			if i != 0:
				query = query + ","

			query = query + "('" + s[self.TYPE_CLIENTS_COLUMM_ID] + "','" + \
						   s[self.TYPE_CLIENTS_COLUMM_TIPO] + "','" + \
						   s[self.TYPE_CLIENTS_COLUMM_DESCONTO] + "')"
			i = i + 1

		self.exec_query(query)

	def carrega_campo(self, valor):
		if valor is not None:
			return valor
		
		return ''

	def processa_tabela_cliente(self, value):
		self.log ("Processando Clientes....")

		self.salva_json_file(value, 'clientes')

		date = datetime.datetime.now()
		timestamp = "%02d/%02d/%04d %02d:%02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute, date.second)

		atualizados = 0
		inseridos = 0

		for s in value:

			result = 0
			nome       = s[self.CLIENTS_COLUMM_NOME].encode('utf-8').decode('utf-8')

			familia = ''
			if s[self.CLIENTS_COLUMM_FAMILIA] is not None:
				familia    = s[self.CLIENTS_COLUMM_FAMILIA].encode('utf-8').decode('utf-8')
				
			tipo       = s[self.CLIENTS_COLUMM_TIPO].encode('utf-8').decode('utf-8')
			data       = self.carrega_campo( s[self.CLIENTS_COLUMM_DATA] )
			ano        = self.carrega_campo( s[self.CLIENTS_COLUMM_ANO] )
			matricula  = self.carrega_campo( s[self.CLIENTS_COLUMM_MATRICULA] )

			pais_1 = ''
			if s[self.CLIENTS_COLUMM_PAIS_1] is not None:
				pais_1     = s[self.CLIENTS_COLUMM_PAIS_1].encode('utf-8').decode('utf-8')

			pais_2 = ''
			if s[self.CLIENTS_COLUMM_PAIS_2] is not None:
				pais_2     = s[self.CLIENTS_COLUMM_PAIS_2].encode('utf-8').decode('utf-8')

			email_1    = self.carrega_campo( s[self.CLIENTS_COLUMM_EMAIL_1])
			email_2    = self.carrega_campo( s[self.CLIENTS_COLUMM_EMAIL_2])
			telefone_1 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_1])
			telefone_2 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_2])
			telefone_3 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_3])
			telefone_4 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_4])
			telefone_5 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_5])
			telefone_6 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_6])
			telefone_7 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_7])
			telefone_8 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_8])
			telefone_9 = self.carrega_campo( s[self.CLIENTS_COLUMM_TELEFONE_9])

			query = """ SELECT count(*) from `""" + self.CLIENTS_TABLE_NAME + """` WHERE `""" \
								 + self.CLIENTS_COLUMM_MATRICULA   + """` = '""" + matricula  + """'"""

			result = self.exec_query(query)

			print("Cadastrando clientes" + str(result))

			if result is not None and result != 0:
	
				atualiza_tudo = False

				# Atualiza tudo
				if atualiza_tudo:
					query_update = """UPDATE `""" + self.CLIENTS_TABLE_NAME + """` SET `""" \
					+ self.CLIENTS_COLUMM_NOME        + """` = '""" + nome       + """', `""" \
					+ self.CLIENTS_COLUMM_FAMILIA     + """` = '""" + familia    + """', `""" \
					+ self.CLIENTS_COLUMM_TIPO        + """` = '""" + tipo       + """', `""" \
					+ self.CLIENTS_COLUMM_DATA        + """` = '""" + data       + """', `""" \
					+ self.CLIENTS_COLUMM_ANO         + """` = '""" + ano	     + """', `""" \
					+ self.CLIENTS_COLUMM_MATRICULA   + """` = '""" + matricula  + """', `""" \
					+ self.CLIENTS_COLUMM_PAIS_1      + """` = '""" + pais_1     + """', `"""\
					+ self.CLIENTS_COLUMM_PAIS_2      + """` = '""" + pais_2     + """', `""" \
					+ self.CLIENTS_COLUMM_EMAIL_1     + """` = '""" + email_1    + """', `""" \
					+ self.CLIENTS_COLUMM_EMAIL_2     + """` = '""" + email_2    + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_1  + """` = '""" + telefone_1 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_2  + """` = '""" + telefone_2 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_3  + """` = '""" + telefone_3 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_4  + """` = '""" + telefone_4 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_5  + """` = '""" + telefone_5 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_6  + """` = '""" + telefone_6 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_7  + """` = '""" + telefone_7 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_8  + """` = '""" + telefone_8 + """', `""" \
					+ self.CLIENTS_COLUMM_TELEFONE_9  + """` = '""" + telefone_9 + """'   """ \
					+ """ WHERE `""" \
					+ self.CLIENTS_COLUMM_MATRICULA + """` = '""" + matricula + """'"""

				else:
					# Atualiza soment nome e email
					query_update = """UPDATE `""" + self.CLIENTS_TABLE_NAME + """` SET `""" \
					+ self.CLIENTS_COLUMM_NOME        + """` = '""" + nome       + """'"""

					if len(email_1) > 0:
						query_update = query_update + """, `""" + self.CLIENTS_COLUMM_EMAIL_1     + """` = '""" + email_1    + """'"""

					if len(email_2) > 0:
						query_update = query_update + """, `""" + self.CLIENTS_COLUMM_EMAIL_2     + """` = '""" + email_2    + """'"""

					query_update = query_update + """ WHERE `""" + self.CLIENTS_COLUMM_MATRICULA + """` = '""" + matricula + """'"""

				result = self.exec_query(query_update)
				atualizados += 1

			else: # result is not None and result == 0:
				query_insert = """ INSERT INTO `""" + self.CLIENTS_TABLE_NAME + """` (
					`""" + self.CLIENTS_COLUMM_NOME       + """`,
					`""" + self.CLIENTS_COLUMM_FAMILIA    + """`,
					`""" + self.CLIENTS_COLUMM_TIPO       + """`,
					`""" + self.CLIENTS_COLUMM_DATA       + """`,
					`""" + self.CLIENTS_COLUMM_ANO        + """`,
					`""" + self.CLIENTS_COLUMM_MATRICULA  + """`,
					`""" + self.CLIENTS_COLUMM_PAIS_1     + """`,
					`""" + self.CLIENTS_COLUMM_PAIS_2     + """`,
					`""" + self.CLIENTS_COLUMM_EMAIL_1    + """`,
					`""" + self.CLIENTS_COLUMM_EMAIL_2    + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_1 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_2 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_3 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_4 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_5 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_6 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_7 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_8 + """`,
					`""" + self.CLIENTS_COLUMM_TELEFONE_9 + """`
					) VALUES ('"""  + \
								nome       + "','" + \
								familia    + "','" + \
								tipo       + "','" + \
								data       + "','" + \
								ano	       + "','" + \
								matricula  + "','" + \
								pais_1     + "','" + \
								pais_2     + "','" + \
								email_1    + "','" + \
								email_2    + "','" + \
								telefone_1 + "','" + \
								telefone_2 + "','" + \
								telefone_3 + "','" + \
								telefone_4 + "','" + \
								telefone_5 + "','" + \
								telefone_6 + "','" + \
								telefone_7 + "','" + \
								telefone_8 + "','" + \
								telefone_9 + "')"
				result = self.exec_query(query_insert)
				inseridos += 1
			
		if result is None:
			return None

		self.log ("Atualizadoss: " + str(atualizados) + " Inseridos: " + str(inseridos))

		return self.db.lastID

	def processa_tabela_produtos(self, value):

		self.salva_json_file(value, 'produtos')
		
		query = """
	   		INSERT INTO `""" + self.PRODUCTS_TABLE_NAME + """` (
		`""" + self.PRODUCTS_COLUMM_ID + """`,
		`""" + self.PRODUCTS_COLUMM_PRODUTO + """`,
		`""" + self.PRODUCTS_COLUMM_VALOR + """`
		) VALUES """

		i=0
		for s in value:
			if i != 0:
				query = query + ","

			query = query + "('" + str(s[self.PRODUCTS_COLUMM_ID]) + "','" + \
											   s[self.PRODUCTS_COLUMM_PRODUTO] + "','" + \
											   s[self.PRODUCTS_COLUMM_VALOR] + "')"
			i = i + 1

		self.exec_query(query)


	def processa_tabela_entradas(self, value):

		self.log ("Processando entradas registradas....")

		self.salva_json_file(value, 'entradas_registradas')

		date = datetime.datetime.now()

		timestamp = "%02d/%02d/%04d %02d:%02d:%02d" % (date.day, date.month, date.year, date.hour, date.minute, date.second)
		
		atualizados = 0
		inseridos = 0

		if value is None:
			self.log("Retornando! value nulo")
			return None

		result = None

		for s in value:

			self.log("Processando... atu: "  + str(atualizados) + " ins: " + str(inseridos))

			data_sem_hora = s[self.INPUT_COLUMN_DATAHORA].split(" ")[0]

			id_org     = str(s[self.INPUT_COLUMN_ID])
			operador   = s[self.INPUT_COLUMN_OPERADOR]
			cliente    = s[self.INPUT_COLUMN_CLIENTE]
			produto    = s[self.INPUT_COLUMN_PRODUTO]
			valor      = s[self.INPUT_COLUMN_VALOR]
			pago       = s[self.INPUT_COLUMN_PAGO]
			removido   = s[self.INPUT_COLUMN_REMOVIDO]
			quantidade = s[self.INPUT_COLUMN_QUANTIDADE]

			seletor = """`""" + self.INPUT_COLUMN_ID_ORG        + """` = '""" + id_org  + """' and 
						 `""" + self.INPUT_COLUMN_CLIENTE       + """` = '""" + cliente + """' and 
						 `""" + self.INPUT_COLUMN_DATAHORA      + """` = '""" + data_sem_hora + """'"""


			query = """ SELECT count(*) from `""" + self.INPUT_TABLE_NAME + """` WHERE """ + seletor

			result = self.exec_query(query)

			if result is not None and result != 0:

				query_update = """UPDATE `""" + self.INPUT_TABLE_NAME + """` SET `""" \
				+ self.INPUT_COLUMN_OPERADOR    + """` = '""" + operador      + """', `""" \
				+ self.INPUT_COLUMN_CLIENTE     + """` = '""" + cliente       + """', `""" \
				+ self.INPUT_COLUMN_PRODUTO     + """` = '""" + produto       + """', `""" \
				+ self.INPUT_COLUMN_VALOR       + """` = '""" + valor         + """', `""" \
				+ self.INPUT_COLUMN_DATAHORA    + """` = '""" + data_sem_hora + """', `""" \
				+ self.INPUT_COLUMN_PAGO        + """` = '""" + pago          + """', `""" \
				+ self.INPUT_COLUMN_REMOVIDO    + """` = '""" + removido      + """', `""" \
				+ self.INPUT_COLUMN_QUANTIDADE  + """` = '""" + quantidade    + """'   """ \
				+ """ WHERE """ + seletor

				result = self.exec_query(query_update)
				atualizados += 1
			else:
				query_insert = """ INSERT INTO `""" + self.INPUT_TABLE_NAME + """` (
										`""" + self.INPUT_COLUMN_ID_ORG + """`,
										`""" + self.INPUT_COLUMN_OPERADOR + """`,
										`""" + self.INPUT_COLUMN_CLIENTE + """`,
										`""" + self.INPUT_COLUMN_PRODUTO + """`,
										`""" + self.INPUT_COLUMN_VALOR + """`,
										`""" + self.INPUT_COLUMN_DATAHORA + """`,
										`""" + self.INPUT_COLUMN_PAGO + """`,
										`""" + self.INPUT_COLUMN_REMOVIDO + """`,
										`""" + self.INPUT_COLUMN_QUANTIDADE + """` 
					) VALUES ('""" + id_org       + "','" + \
									operador      + "','" + \
									cliente       + "','" + \
									produto       + "','" + \
									valor         + "','" + \
									data_sem_hora + "','" + \
									pago          + "','" + \
									removido      + "','" + \
									quantidade    + "')"

				result = self.exec_query(query_insert)
				try:
					self.log (str(inseridos) + ": cliente: " + cliente + " produto: " + produto + " valor: " + valor)
				except Exception as e:
					self.log("ERRO: " + str(e))

				inseridos += 1

		if result is None:
			return None

		self.log ("Atualizados: " + str(atualizados) + " Inseridos: " + str(inseridos))

		return self.db.lastID

	def processa_tabela_config(self, value):
		query = """            
	   		INSERT INTO `""" + self.CONFIG_TABLE_NAME + """` (
		`""" + self.CONFIG_COLUMN_ID + """`,
		`""" + self.CONFIG_COLUMN_INFO + """`,
		`""" + self.CONFIG_COLUMN_VALUE + """`
		) VALUES """

		i=0
		for s in value:
			if i != 0:
				query = query + ","

			query = query + "('" + s[self.CONFIG_COLUMN_ID] + "','" + \
						   s[self.CONFIG_COLUMN_INFO] + "','" + \
						   s[self.CONFIG_COLUMN_VALUE] + "')"
			i = i + 1

		self.exec_query(query)

	def getDataTable (self, table):
		query = """
				SELECT * FROM `%s`
				WHERE 1
				""" % table

		dump_table = self.exec_query(query, 'json')
		dump_json = json.dumps(dump_table)
		result = "{\"%s\":%s}" % (table, dump_json)
		return result

	def getBalanceDataTable (self):
		query = """
				SELECT `""" + self.BALANCE_ID + """`,
					   `""" + self.BALANCE_NAME + """`, 
					   `""" + self.BALANCE_REAL + """`,
					   `""" + self.BALANCE_REAL_DATE + """`				
				FROM `""" + self.BALANCE_TABLE_NAME + """`
				WHERE 1 """

		dump_table = self.exec_query(query, 'json')
		dump_json = json.dumps(dump_table)
		result = "{\"%s\":%s}" % (self.BALANCE_TABLE_NAME, dump_json)
		return result

	
	def getDataTableToCsv (self, table):
		date = datetime.datetime.now()
		timestamp = "%02d%02d%04d-%02d%02d%02d" % (date.day, date.month, date.year, date.hour, date.minute, date.second)
		query = """
				SELECT * FROM `%s`
				INTO OUTFILE '/tmp/%s_%s.csv'
				""" % (table,table,timestamp)

		return self.exec_query(query, 'csv')

	def cadastraEntradasRegistradas (self, nome, produto, quantidade, valor, timestamp):

		id_org = randint (1000, 9999)
		data = [ { self.INPUT_COLUMN_ID : str(id_org),
				self.INPUT_COLUMN_OPERADOR : "automacao",
				self.INPUT_COLUMN_CLIENTE : str(nome),
				self.INPUT_COLUMN_PRODUTO : produto,
				self.INPUT_COLUMN_VALOR : str(valor),
				self.INPUT_COLUMN_DATAHORA : str(timestamp),
				self.INPUT_COLUMN_PAGO : "Aberto",
				self.INPUT_COLUMN_REMOVIDO : "NAO",
				self.INPUT_COLUMN_QUANTIDADE : str(quantidade) } ]

		self.log(str(data))

		lastid = self.processa_tabela_entradas(data)

		if lastid is not None:
			return self.getEntradaRegistrada(lastid)

		return {"Entradas_Registradas":data}

	def getNameFromMatr (self, idBarCode):
		query = """
				SELECT `""" + self.CLIENTS_COLUMM_NOME + """` FROM `""" + self.CLIENTS_TABLE_NAME + """`
				WHERE `""" + self.CLIENTS_COLUMM_MATRICULA + """` = \"%s\"
				""" % idBarCode

		nome = self.getValueOfTable(query)

		if nome == 0:
			nome = "Matricula nao identificada"

		return nome
	
	def getMatrFromName (self, nome):
		query = """
				SELECT `""" + self.CLIENTS_COLUMM_MATRICULA + """` FROM `""" + self.CLIENTS_TABLE_NAME + """`
				WHERE `""" + self.CLIENTS_COLUMM_NOME + """` = \"%s\"
				""" % nome

		matricula = self.getValueOfTable(query)

		if matricula == 0:
			matricula = "Matricula nao identificada"

		return matricula

	def getTypeClientFromMatr (self, idBarCode):
		query = """
				SELECT `""" + self.CLIENTS_COLUMM_TIPO + """` FROM `""" + self.CLIENTS_TABLE_NAME + """`
				WHERE `""" + self.CLIENTS_COLUMM_MATRICULA + """` = \"%s\"
				""" % idBarCode

		return self.getValueOfTable(query)

	def getTypeClientFromName (self, name):
		query = """
				SELECT `""" + self.CLIENTS_COLUMM_TIPO + """` FROM `""" + self.CLIENTS_TABLE_NAME + """`
				WHERE `""" + self.CLIENTS_COLUMM_NOME + """` = \"%s\"
				""" % name

		return self.getValueOfTable(query)

	def getValueOfProduct (self, product):
		query = """
				SELECT `""" + self.PRODUCTS_COLUMM_VALOR + """` FROM `""" + self.PRODUCTS_TABLE_NAME + """`
				WHERE `""" + self.PRODUCTS_COLUMM_PRODUTO + """` = \"%s\"
				""" % product

		return self.getValueOfTable(query)

	def getDiscontoOfClientType (self, tipo_cliente):
		query = """
				SELECT `""" + self.TYPE_CLIENTS_COLUMM_DESCONTO + """` FROM `""" + self.TYPE_CLIENTS_TABLE_NAME + """`
				WHERE `"""  + self.TYPE_CLIENTS_COLUMM_TIPO + """` = \"%s\"
				""" % tipo_cliente

		return self.getValueOfTable(query)

	def getValueOfTable(self, query):
		resultado = self.exec_query(query, 'csv')
		
		if resultado is not None:
			if len(resultado) == 0:
				self.log ( "Item nao esta cadastrado")
				
				return 0

			if len(resultado) > 1:
				self.log ( "Item duplicado")
				return 0
				
			for r in resultado:
				return r[0]
		
		return 0

	def getEntradaRegistrada (self, id):

		query = """
				SELECT * FROM `""" + self.INPUT_TABLE_NAME + """`
				WHERE """ + self.INPUT_COLUMN_ID + """ = \"%s\"
				""" % id

		dump_table = self.exec_query(query, 'json')
		return {"Entradas_Registradas": dump_table}

	def getEntradasRegistradas (self, data):

		query = """
				SELECT * FROM `""" + self.INPUT_TABLE_NAME + """`
				WHERE """ + self.INPUT_COLUMN_DATAHORA + """ = \"%s\" 
				""" % data

		dump_table = self.exec_query(query, 'json')
		# dump_json = json.dumps(dump_table)
		return {"Entradas_Registradas": dump_table}

	def getAllEntradasRegistradas (self,data):

		query = """
				SELECT * FROM `""" + self.INPUT_TABLE_NAME + """`
				WHERE """ + self.INPUT_COLUMN_DATAHORA + """ = \"%s\" 
				""" % data 

		return self.exec_query(query,'csv')

	def getAllEntradasRegistradasPagas (self,data):

		query = """
				SELECT * FROM `""" + self.INPUT_TABLE_NAME + """`
				WHERE `""" + self.INPUT_COLUMN_DATAHORA + """` = \"""" + data + """\" and 
					  """ + self.INPUT_COLUMN_PAGO + """ = \"SIM\" 
						  and `removido` = \"NAO\" and `cliente` != \"LUCAS NOTO COLTRO\"
				"""

		return self.exec_query(query,'csv')

	def alteraEntradasRegistradas (self, id, campo, valor):
		query = """
			UPDATE `Entradas_Registradas` SET `%s` = '%s' WHERE `Entradas_Registradas`.`id` = %s
				""" % (campo,valor,id)
		
		if self.exec_query(query) is not None:
			return self.getEntradaRegistrada(id)

		self.log( "ERRO ao alterar entrada_registrada " % campo)
		return None

	def apagaEntradaRegistrada (self, id):
		query = """
			DELETE FROM `Entradas_Registradas` WHERE `Entradas_Registradas`.`id` = %s 
				""" % str(id)

		if self.exec_query(query) is not None:
			return True

		return False

	def existeDeposito (self, id):
		query = """
				SELECT count(*) FROM `""" + self.INPUT_TABLE_NAME + """`
				WHERE """ + self.INPUT_COLUMN_ID_ORG + """ = \"""" + str(id) + """\" and 
					  """ + self.INPUT_COLUMN_PRODUTO + """ = \"DEPOSITO\"
				"""
		result = self.exec_query(query)

		if result is not None and result != 0:
			return True

		return False

	def realizaDeposito(self, id, nome, data, valor):

		if self.existeDeposito(id) is False:

			query = """
				INSERT INTO `Entradas_Registradas` 
				(`id_org`,`operador`,`cliente`,`produto`,`valor`,`datahora`,`pago`,`removido`,`quantidade`) 
				VALUES (
				'""" + id + """',
				'automacao',
				'""" + nome + """',
				'DEPOSITO',
				'""" + str(valor) + """',
				'""" + data + """',
				'DEPOSITO','fechado','1'
				)
				"""
			return self.exec_query(query)

		self.log ("Ja existe deposito deste valor com este identificacao " + str(id))
		return None

	def getInfoAllClients (self):
		query = """
				SELECT cliente_nome, cliente_email_1, cliente_matricula FROM `Clientes` where 1 ORDER BY cliente_nome DESC
				"""
		return self.exec_query(query, 'csv')

	def getListOfRegister (self, cliente, data_inicial=None):
		query = "SELECT produto, valor, datahora, pago FROM `Entradas_Registradas` WHERE \
						`cliente` = \"" + cliente + "\" and \
						`pago` not like \"Informa%\" and \
						`produto` != \"Ajuste saldo\" and \
						`removido` != \"SIM\" "

		if data_inicial is not None:
			query = query + """ and str_to_date(`datahora`, '%d/%m/%Y') >=	 str_to_date('""" + data_inicial + """', '%d/%m/%Y')"""
	  
	  	query = query + """ ORDER BY str_to_date(`datahora`, '%d/%m/%Y') ASC"""

		return self.exec_query(query, 'csv')

	def setInfoEmailEnviado(self, nome, saldo, data_envio):

		query = """
			INSERT INTO `Entradas_Registradas` 
			(`id_org`,`operador`,`cliente`,`produto`,`valor`,`datahora`,`pago`,`removido`,`quantidade`) 
			VALUES (
			'0',
			'email',
			'""" + nome + """',
			'Email encaminhado (informacao de saldo)',
			'""" + str(saldo) + """',
			'""" + data_envio + """',
			'Informacao','fechado','0'
			)
			"""
		return self.exec_query(query)

	def insereSaldoCliente(self, nome, matricula, saldo_inicial, saldo_real, data_inicial, data_final, data_real):

		query = """
			INSERT INTO `""" + self.BALANCE_TABLE_NAME + """` (
				`""" + self.BALANCE_NAME + """`, 
				`""" + self.BALANCE_MATRICULA + """`, 
				`""" + self.BALANCE_INITIAL + """`,
				`""" + self.BALANCE_INITIAL_END_DATE + """`,
				`""" + self.BALANCE_INITIAL_START_DATE + """`,
				`""" + self.BALANCE_REAL + """`,
				`""" + self.BALANCE_REAL_DATE + """`)  
			VALUES (
			'""" + nome + """',
			'""" + matricula + """',
			'""" + saldo_inicial + """',
			'""" + data_inicial + """',
			'""" + data_final + """',
			'""" + saldo_real + """',
			'""" + data_real + """')"""

		return self.exec_query(query)

	def atualizaSaldoCliente(self, nome, saldo_real, data_real):
		query = """
			UPDATE `""" + self.BALANCE_TABLE_NAME + """` SET 
				   `""" + self.BALANCE_REAL       + """` = '""" + saldo_real + """',
				   `""" + self.BALANCE_REAL_DATE  + """` = '""" + data_real + """'
			WHERE `""" + self.BALANCE_NAME + """` = '""" + nome + """'"""
		
		return self.exec_query(query)

	def getSaldoClienteDeSaldos (self, nome):
		query = """
			SELECT `""" + self.BALANCE_INITIAL + """` from `""" + self.BALANCE_TABLE_NAME + """` where
				`""" + self.BALANCE_NAME + """` = '%s' """ % (nome)
		
		return self.exec_query(query)

	def getDateLastEventEntradasRegistradas(self):
		query = """
			SELECT `""" + self.INPUT_COLUMN_DATAHORA + """` from `""" + self.INPUT_TABLE_NAME + """` order by id desc limit 1"""
		
		return self.exec_query(query)

	def getSaldoCliente (self, nome, data_corte = None):

		# calcula o saldo no periodo
		# Credito -> 'pago' = DEPOSITO
		# Debito  -> 'pago' = Aberto
		# Nao contabiliza -> 'pago' = Pagou
		# Nao contabiliza -> 'removido' = SIM
		# Nao contabiliza -> 'removido' = fechado

		query = """
			SELECT datahora, pago, valor from `Entradas_Registradas`
			where `cliente` = \"""" + nome + """\" and
			`pago` not like \"Informa%\" and 
			`produto` != \"Ajuste saldo\" and
			`removido` != \"SIM\"
			"""
	  
	  	query = query + """ ORDER BY str_to_date(`datahora`, '%d/%m/%Y'	) ASC"""

		# Primeiro registro, eh o mais antigo!
		resultado = self.exec_query(query, 'csv')

		# Saldo inicial
		saldo_inicial = float(self.getSaldoClienteDeSaldos (nome))

		credito   = 0
		debito    = 0
		contador  = 0

		# Inicial <---> Anterior <----> Final

		saldo_anterior = 0
		saldo_final    = 0
		saldo_periodo  = 0
		primeira_data  = ''
		ultima_data    = ''

		dCorte = None
		if data_corte is not None:
			dCorte=time.strptime(data_corte, "%d/%m/%Y")

	#	try:

		for r in resultado:

			datahora = r[0]
			pago     = r[1]
			valor    = r[2]

			if valor is None or valor == '':
				continue

			ultima_data = datahora.split(' ')[0]
			dRegistro = time.strptime(ultima_data, "%d/%m/%Y")

			if dCorte is not None and dCorte > dRegistro:
				# contabilizando consumo do inicio ate a data de corte
				if pago == "DEPOSITO":
					saldo_anterior += float(valor)
				else:
					saldo_anterior -= float(valor)
			else:
				# contabilizando consumo da data de corte ate o fim
				contador = contador + 1
				if contador == 1:
					primeira_data = datahora.split(' ')[0]

				if pago == "DEPOSITO":
					credito += float(valor)
				else:
					debito += float(valor)

			# print str(contador) + " | " + str(datahora) + " -> " + str(primeira_data)

		saldo_periodo = float("{0:.2f}".format(credito - debito))
		saldo_anterior += saldo_inicial 
		saldo_final = saldo_anterior + saldo_periodo

		# except Exception, e:
		# 	self.log   ("Erro no tratamento do valor para " + nome)
		# 	self.log  (e)

	  	return credito, debito, contador, primeira_data, ultima_data, saldo_anterior, saldo_periodo, saldo_final


	def popula_tabela_saldos(self, inicial = False):
		self.log ("Populando tabela saldo...")

		#cliente_nome, cliente_email_1, cliente_matricula 
		clientes = self.getInfoAllClients()

		for cliente in clientes:

			if cliente[0] is None:
				self.log  ("sem nome")
				continue
			
			if cliente[2] is None or (cliente[2] is not None and len(cliente[2]) < 2):
				self.log  (cliente[0] + " sem matricula")

			# if cliente[1] is None or (cliente[1] is not None and len(cliente[1]) < 5):
			#	self.log  (cliente[0] + " sem email")

			nome = cliente[0].encode('utf-8').decode('utf-8')
			matricula = cliente[2]

			creditos, debitos, contador, primeira_data, ultima_data, saldo_inicial, saldo, saldo_final =  self.getSaldoCliente(nome)

			if saldo > -0.5 and saldo < 0.5:
				saldo = 0

			if inicial:
				self.insereSaldoCliente(nome, matricula, str(saldo), str(saldo), primeira_data, ultima_data, ultima_data)

			else:
				sini = float(self.getSaldoClienteDeSaldos(nome))
				saldo_inicial = float("{0:.2f}".format(sini))
				saldo_real  =  saldo_inicial + float("{0:.2f}".format(saldo))
				self.atualizaSaldoCliente(nome, str(saldo_real), str(ultima_data)) 

				#if saldo != 0:
				#	print "Ini:" + str(saldo_inicial) + " Saldo: " + str(saldo) + " Real: " + str(saldo_real)

		self.log ("concluido! ")

	def salva_json_file(self, value, name):
		date = datetime.datetime.now()
		timestampfile = "/home/ubuntu/BACKUP/%02d%02d%04d_%02d%02d%02d" % (date.day, date.month, date.year, date.hour, date.minute, date.second)
		try:
			jfile = "/home/ubuntu/BACKUP/%s_%02d%02d%04d_%02d%02d%02d" % (name, date.day, date.month, date.year, date.hour, date.minute, date.second)
			with open(jfile, 'w') as outfile:  
				json.dump(value, outfile)
			self.log ("Salvou arquivo: jfile")

		except Exception as e:
			self.log("ERRO ao salvar o JSON: " + str(e))



