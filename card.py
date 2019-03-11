# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re


class Card(object):

	__CARD_PAGE = 'https://2dkf.com/kf_fw_ig_mycard.php'
	
	def __init__(self, user, log = None):
		self.safeid = user.safeid
		self.req = user.req
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log
		

	def getCard(self):
		self.log.info('--开始领取卡片--')
		growupUrl = self.__CARD_PAGE + '?card=new&safeid=' + self.safeid
		res = self.req.get(growupUrl)
		self.log.info('--领取卡片结束--')
		self.log.info()