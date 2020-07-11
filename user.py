# -*- coding: UTF-8 -*-
from req import KfReq
from log import Logging
from lxml import etree
import re

import constants

class User:

	__LOGIN_PAGE = constants.DOMAIN + '/login.php'

	__INDEX_PAGE = constants.DOMAIN + '/'

	__SAFEID_PAGE = constants.DOMAIN + '/kf_fw_ig_index.php'


	__SM_PAGE = constants.DOMAIN + '/kf_growup.php'

	def __init__(self, username, password, log = None):
		self.loginStatus = False
		self._safeid = None
		self.username = username
		self.password = password
		self.req = KfReq()
		if log is None:
			self.log = Logging(username)
		else:
			self.log = log

	def login(self):
		self.log.info('--开始登录--')
		self.log.info('username:' + self.username)
		self.log.info('password:' + self.password)
		
		payload = dict(
			jumpurl= self.__INDEX_PAGE,
			step= 2,
			lgt= 1,
			hideid= 0,
			cktime= 31536000,
			pwuser= self.username.encode('GBK'),
			pwpwd=self.password,
			submit='登录'.encode('GBK')
		)
		res = self.req.post(self.__LOGIN_PAGE, data=payload)
		self._safeid = None
		if '您已经顺利登' in res:
			self.log.info('登录成功')
			self.log.info('Cookies: ')
			self.log.info(str(self.req.cookies))
			self.log.info('')
			self.loginStatus = True
			return True
		else:
			self.log.info('登录失败')
			self.loginStatus = False
			return False

	def getSafeid(self):
		self.log.info('--开始获取safeid--')
		res = self.req.get(self. __SAFEID_PAGE)
		htmlTree = etree.HTML(res)
		jsCode = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/script[2]/text()')[0]
		_safeid = re.search("\"safeid=(.*)\"", jsCode).group(1)
		self.log.info('成功获取safeid: ' + _safeid)
		return _safeid

	def reloadSafeid(self):
		self._safeid = self.getSafeid()

	def getSM(self):
		self.log.info('--开始获取神秘系数--')
		res = self.req.get(self. __SM_PAGE)
		htmlTree = etree.HTML(res)
		sm = ''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[1]/div[1]/text()'))
		sm = re.search('.*神秘系数\s(\d*).*', sm).group(1)
		self.log.info('--成功获取神秘系数:' + sm +'--')
		return int(sm)

	@property
	def safeid(self, force=False):
		if self.loginStatus:
			if self._safeid == None or force:
				self._safeid = self.getSafeid()
			return self._safeid
		else:
			self.log.error('未登录账号')