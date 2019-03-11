# -*- coding: UTF-8 -*-
import datetime
import os

class Logging(object):

	def __init__(self, username):
		self.username = username

	def print(self, str):
		print(str)

	def close(self):
		self.f.close()
		
	def info(self, str=''):
		newStr = '[' + datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S') + ']' + '[' + self.username + ']' + str
		self.print(newStr)

	def error(self, str=''):
		self.print('[' + datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S') + ']' + '[' + self.username + ']' + str)