# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re

class Equip(object):

	__EQUIP_PAGE = 'https://2dkf.com/kf_fw_ig_mybp.php'
	__EQUIP_SMELT_PAGE = 'https://2dkf.com/kf_fw_ig_mybpdt.php'

	__EQUIP_NAME = ['普通', '幸运', '稀有', '传奇']

	def __init__(self, user, smeltType, log = None):
		self.safeid = user.safeid
		self.smeltType = smeltType
		self.req = user.req
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log


	def getEquipList(self):
		equipListRes = self.req.get(self.__EQUIP_PAGE)
		htmlTree = etree.HTML(equipListRes)
		equipIds = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[5]/table/tr/td[1]/@id')
		equipNames = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[5]/table/tr/td[3]/span[1]/text()')

		equipList = []
		for i in range(0, len(equipIds)):
			equipList.append(dict(id=re.search('(\d*)$', equipIds[i]).group(1), name=equipNames[i]))
		return equipList

	def genMatchRegex(self, matchType=None):
		if matchType is None:
			matchType=self.smeltType
		regexStr = '^('
		for i in range(0, len(matchType)):
			if matchType[i]:
				regexStr += (self.__EQUIP_NAME[i] + '|')
		if len(regexStr) != 2:
			regexStr = regexStr[0: len(regexStr)-1]
		regexStr += ')'
		return regexStr

	def smeltEquip(self, id):
		payload = dict(
			do=5,
			id=id,
			safeid=self.safeid
		)
		smeltRes = self.req.post(self.__EQUIP_SMELT_PAGE, data=payload)
		return smeltRes


	def autoSmelt(self):
		self.log.info('--开始自动熔炼--')
		matchRegex = self.genMatchRegex()
		while True:
			equipList = self.getEquipList()
			beforeSize = len(equipList)
			for equip in equipList:
				if re.match(matchRegex, equip['name']):
					self.smeltEquip(equip['id'])
					equipList.remove(equip)
					self.log.info('熔炼:\t' + equip['name'] + '\t' + equip['id'])
			if beforeSize == len(equipList):
				break
		self.log.info('--自动熔炼结束--')
		self.log.info()