#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class MontaEmailCliente():

	def __init__(self, nome, email, logging = None):
		self.logging       = logging
		self.nome          = nome
		self.email         = email

	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print msg

	def MessageColetiva (self, arq_html):
		with open(arq_html, 'r') as f:
			self.message = f.read()

	def MessageClient (self, db, saldo_anterior, saldo_final, primeira_data, ultima_data):
		self.saldo_final    = saldo_final
		self.saldo_anterior = saldo_anterior
		self.primeira_data  = primeira_data
		self.ultima_data    = ultima_data

		self.message  = "<html><body>"
		self.message  += "Olá <br />"
		self.message  += "Segue o saldo da cantina para o aluno: " + self.nome
		self.message  += "<dd>Saldo anterior: R$ " + str(format(float(self.saldo_anterior),'.2f'))
		self.message  += "<dd>Saldo final: R$ " + str(format(float(self.saldo_final),'.2f'))
		self.message  += "<dd>Período: " + str(self.primeira_data) + " até " + str(self.ultima_data) + "</dd>"
		self.message  += "O relatório do consumo esta anexado. <br />"
		self.message  += "<b>IMPORTANTE:</b> Mudou o Banco/Conta para fazer depósito. <br />"

		if self.saldo_final < 0:
			self.MessageDevedor()

		self.Message(db)	

	def MessageDevedor (self):
		self.message  += "<br />Se preferir fazer depósito, favor encaminhar o comprovante para <b>cantinadafamilia@hotmail.com </b>após fazê-lo."
		self.message  += "<font size=\"2\"><br /><div>"
		self.message  += "<table border=0 width=\"60%\" cellspacing=\"3\" cellpadding=\"1\">"
		self.message  += "<tr><td><b> Banco:          </b></td><td> Banco Itaú  (banco 341)   </td></tr>"
		self.message  += "<tr><td><b> Cliente:        </b></td><td> Cantina da Família EIRELI </td></tr>"
		self.message  += "<tr><td><b> Agência:        </b></td><td> 1575                    </td></tr>"
		self.message  += "<tr><td><b> Conta Corrente: </b></td><td> 23617-7                 </td></tr>"
		self.message  += "<tr><td><b> CNPJ:           </b></td><td> 09.373.276/0001-90      </td></tr>"
		self.message  += "</table></font><br /></div>"

	def Message (self, db):

		self.message  += "<br />Att."
		self.message  += "<br />Cantina do Dindo<br /> --------------------------------------------<br />"

		resultado = db.getListOfRegister(self.nome, self.primeira_data.encode('ascii', 'ignore'))

		self.message += "<font size=\"2\"><br />"
		self.message += "<table border=0 width=\"60%\" cellspacing=\"3\" cellpadding=\"1\">"
		self.message += "<tr>"
		self.message += "<td><b> Produto    </b></td>"
		self.message += "<td align=\"right\"><b> Valor (R$) </b></td>"
		self.message += "<td align=\"right\"><b> Data hora  </b></td>"
		#self.message += "<td><b> Pago      </b></td>";
		self.message += "</tr>"

		self.message += "<tr>"
		self.message += "<td>Saldo anterior</td>"
		self.message += "<td align=\"right\">" + str(format(float(self.saldo_anterior),'.2f')).encode('ascii', 'ignore') + " </td>"
		self.message += "<td align=\"right\">" + self.primeira_data.encode('ascii', 'ignore') + " </td>"
		#self.message += "<td> Informacao </td>"
		self.message += "</tr>"

		for r in resultado:
			valor = format(float(r[1]),'.2f')
			self.message += "<tr>"
			self.message += "<td>" + r[0].encode('utf8') + " </td>"
			self.message += "<td align=\"right\">" + valor.encode('ascii', 'ignore') + " </td>"
			self.message += "<td align=\"right\">" + r[2].encode('ascii', 'ignore') + " </td>"
			#self.message += "<td>" + r[3].encode('ascii', 'ignore') + " </td>";
			self.message += "</tr>"

		self.message += "</table>"
		self.message += "<br />Total: R$ "+ str(format(float(self.saldo_final),'.2f')) + "</font><br />"
		self.message += "</html></body>"

#
# Process init
#

if __name__ == '__main__':
	print "Inicia montagem da mensagem"

	nome = "Paulo Alex Dariva"
	saldo = 0
	primeira_data = "10/02/2018"
	ultima_data = "18/12/2018"
	email = "dariva@gmail.com"

	msg = MontaEmailCliente(nome, saldo, primeira_data, ultima_data, email)
	msg.Message()
