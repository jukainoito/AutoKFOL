# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re


class Shop(object):

	__SHOP_PAGE = 'https://2dkf.com/kf_fw_ig_shop.php'

	__SHOP_ITEM = {'101':'等级经验药丸', '102':'等级经验药丸（蛋）'}

	def __init__(self, user, log = None):
		self.safeid = user.safeid
		self.req = user.req
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log
		
	def getCurMoney(self):
		res = self.req.get(self.__SHOP_PAGE)
		htmlTree = etree.HTML(res)
		kfbStr = (''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[1]/div[1]/a[2]/text()')))
		return int(re.search('^(\d*)KFB', kfbStr).group(1))

	def buy(self, id):
		payload = dict(
			buy=id,
			safeid=self.safeid
		)
		res = self.req.post(self.__SHOP_PAGE, data=payload)
		return res

	def autoBuy(self):
		self.log.info('--开始自动购买经验--')
		kfb = self.getCurMoney()
		self.log.info('当前KFB: ' + str(kfb))
		while True:
			buyId = -1
			used = 0
			if kfb >= 10000:
				buyId = '102'
				used = 10000
			elif kfb >= 5000:
				buyId = '101'
				used = 5000
			else:
				break
			self.buy(buyId)
			self.log.info(str(kfb) + '\t' + self.__SHOP_ITEM[buyId] + '\tUSED' + str(used) + '\t' + str(kfb-used))
			kfb = kfb - used
		self.log.info('--自动购买经验结束--')
		self.log.info()