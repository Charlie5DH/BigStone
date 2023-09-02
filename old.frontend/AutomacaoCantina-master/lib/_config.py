#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import ConfigParser
import logging

class IniSett():

	def __init__(self,inifile = None):
		if inifile is None: return None
		self.file_path = inifile

		self.Config = ConfigParser.ConfigParser()
		self.Config.read(self.file_path)
		#Config.get('Directories', 'img_dir')

	def get(self, section, param):
		return self.Config.get(section, param)

	def set(self, section, key, value):
		self.Config.set(section, key, value)
		self.commit()

	def append(self, section, key, value):
		values = self.get(section, key).split(',')
		values.append(value.strip())
		self.set(section, key, ','.join(values))
		self.commit()

	def remove(self, section, key, value):
		list_str = self.get(section, key)
		values = list_str.split(',')
		values.remove(value.strip())
		self.set(section, key, ','.join(values))
		self.commit()

	def commit(self):
		configfile = open(self.file_path, 'wb')
		self.Config.write(configfile)
		self.Config.read(self.file_path)