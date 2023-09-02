#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
class EmailClient():

	def __init__(self, server, smtp_port, fromaddr, password, fromname = None, logging = None):
		self.logging   = logging
		self.server    = server
		self.smtp_port = smtp_port
		self.fromaddr  = fromaddr
		self.fromname  = fromname
		self.log ("EmailClient INIT")

		try:
			self.cli_smtp = smtplib.SMTP(self.server, self.smtp_port)
			self.cli_smtp.starttls()

			self.cli_smtp.login(self.fromaddr, password)

		except smtplib.SMTPAuthenticationError:
			self.log ("Erro de autenticacao")
			return None

		except smtplib.SMTPException:
			self.log ("Erro de conexao")
			return None


	def emailsend (self, toaddr, subject, body, ccaddr = None, bccaddr = None):
		self.msg = MIMEMultipart()

		self.msg['From']    = str(self.fromname) + "<" + str(self.fromaddr) + ">"
		self.msg['To']      = toaddr
		self.toaddrs = toaddr

		if ccaddr is not None:
			self.msg['Cc']      = ccaddr
			self.toaddrs = self.toaddrs + "," + ccaddr

		if bccaddr is not None:
			self.msg['Bcc']     = bccaddr
			self.toaddrs = self.toaddrs + "," + bccaddr

		self.msg['Subject'] = subject

		self.msg.attach(MIMEText(body, 'html'))
		self.text = self.msg.as_string()

		try:
			self.cli_smtp.sendmail(self.fromaddr, self.toaddrs.split(","), self.text)

		except smtplib.SMTPException:
			self.log ("Erro no envio")
			return False

		except Exception as e:
			return False

		return True
 

	def close (self):
		self.cli_smtp.quit()

	def log (self,msg):
		if self.logging is not None:
			self.logging.info (msg)
		else:
			print msg

if __name__ == '__main__':

	print "Iniciando email"

	server    = 'smtp.gmail.com'
	smtp_port = 587
	fromaddr  = "cantinadodindo@gmail.com"
	fromname  = "Cantina do Dindo"
	toaddr    = "dariva@gmail.com"

	password = raw_input('Digite a senha do email para ' + fromaddr + ':')


	eml = EmailClient(server, smtp_port, fromaddr, password, fromname)

	if eml is not None:

		subject = 'Testando classe de email'
		body = 'Este é o corpo do teste'

		c = eml.emailsend (toaddr, subject, body)

		if c:
			eml.close()
			print "Sucesso!"

		else:
			print "Erro no envio da mensagem"


