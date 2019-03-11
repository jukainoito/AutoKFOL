# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re
import time



class Box(object):

	__BOX_PAGE = 'https://2dkf.com/kf_fw_ig_mybp.php'
	__BOX_OPEN_PAGE = 'https://2dkf.com/kf_fw_ig_mybpdt.php'

	def __init__(self, user, boxType, log=None):
		self.safeid = user.safeid
		self.req = user.req
		self.boxType = boxType
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log


	def getBoxQuantity(self):
		res = self.req.get(self.__BOX_PAGE)
		htmlTree = etree.HTML(res)
		return [
			int(''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/table/tr[2]/td[1]/span[2]/text()'))),
			int(''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/table/tr[2]/td[2]/span[2]/text()'))),
			int(''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/table/tr[2]/td[3]/span[2]/text()'))),
			int(''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/table/tr[2]/td[4]/span[2]/text()')))
		]

	def openSingleBox(self, openBoxType):
		payload = dict(
			do=3,
			id=openBoxType,
			safeid=self.safeid
		)
		openRes = self.req.post(self.__BOX_OPEN_PAGE, data=payload)
		return openRes

	def openBox(self):
		boxQuantity = self.getBoxQuantity()
		for i in range(0, 4):
			if self.boxType[i]:
				for n in range(0, boxQuantity[i]):
					openRes = self.openSingleBox(i+1)
					self.log.info(str(i+1)+':\t'+openRes)
					time.sleep(1)


	def autoOpenBox(self):
		self.log.info('--开始自动开盒--')
		self.log.info('获取盒子数:')
		boxQuantity = self.getBoxQuantity()
		self.log.info(' '.join(map(str, boxQuantity)))
		self.log.info('开始打开盒子')
		self.openBox()
		self.log.info('--自动开盒结束--')
		self.log.info()