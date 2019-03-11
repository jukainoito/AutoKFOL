# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re

import time

class Item(object):



	__ITEM_NAME_LIST = ['蕾米莉亚同人漫画','十六夜同人漫画','档案室钥匙','傲娇LOLI娇蛮音CD','消逝之药','整形优惠卷']
	__ITEM_PAGE = 'https://2dkf.com/kf_fw_ig_mybp.php'
	__ITEM_USE_SELL_PAGE = 'https://2dkf.com/kf_fw_ig_mybpdt.php'

	def __init__(self, user, useType, sellType, log = None):
		self.safeid = user.safeid
		self.req = user.req
		self.useType = useType
		self.sellType = sellType
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log

	def getItemTypeByName(self, name):
		for i in range(0, len(self.__ITEM_NAME_LIST)):
			if name == self.__ITEM_NAME_LIST[i]:
				return i

	def getItemList(self):
		res = self.req.get(self.__ITEM_PAGE)
		htmlTree = etree.HTML(res)
		itemIds = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[7]/table/tr/@id')
		itemNames = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[7]/table/tr[(@id)]/td[3]/text()')
		itemList = []
		for i in range(0, len(itemIds)):
			itemList.append(dict(id=re.search('(\d*)$', itemIds[i]).group(1),
				name=itemNames[i],
				type=self.getItemTypeByName(itemNames[i])))
		return itemList

	def useItem(self, id):
		payload = dict(
			do=1,
			id=id,
			safeid=self.safeid
		)
		useRes = self.req.post(self.__ITEM_USE_SELL_PAGE, data=payload)
		return useRes


	def sellItem(self, id):
		payload = dict(
			do=2,
			id=id,
			safeid=self.safeid
		)
		sellRes = self.req.post(self.__ITEM_USE_SELL_PAGE, data=payload)
		return sellRes

	def autoItemCommand(self):
		self.log.info('--开始自动处理道具--')
		itemList = self.getItemList()
		self.log.info('获取道具列表,共有 ' + str(len(itemList)))
		for item in itemList:
			if self.useType[item['type']]:
				ret = self.useItem(item['id'])
				self.log.info(ret)
				self.log.info(str(item['name']) + '\t' + item['id'] + '\t USE')
			elif self.sellType[item['type']]:
				ret = self.sellItem(item['id'])
				self.log.info(ret)
				self.log.info(str(item['name']) + '\t' + item['id'] + '\t SELL')
			time.sleep(2)
		self.log.info('--自动处理道具结束--')
		self.log.info()