# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re

import constants

class Growup(object):

	__GROWUP_PAGE = constants.DOMAIN + '/kf_growup.php'
	
	def __init__(self, user, log = None):
		self.user = user
		self.req = user.req
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log

	def growup(self):
		self.user.reloadSafeid()
		self.safeid = self.user.safeid
		self.log.info('--开始领取登录奖励--')
		growupUrl = self.__GROWUP_PAGE + '?ok=3&safeid=' + self.safeid
		res = self.req.get(growupUrl)
		self.log.info('--领取登录奖励结束--')
		self.log.info()