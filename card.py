# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from lxml import etree
import re
import sys

import constants


class Card(object):

	__CARD_PAGE = constants.DOMAIN + '/kf_fw_ig_mycard.php'
	
	def __init__(self, user, log = None):
		self.safeid = user.safeid
		self.req = user.req
		self.user = user
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log
	
	def getNowCard(self):
		self.log.info('--开始获取现有卡片信息--')
		res = self.req.get(self.__CARD_PAGE)
		cardHtml = etree.HTML(res)
		cardTable = cardHtml.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/div[2]/table/tr')
		cardList = []
		for card in cardTable:
			level = ''.join(card.xpath('td[1]/div/text()'))
			if len(level) == 0:
				continue
			level = re.search(".*等级上限\s(\d*).*", level).group(1)
			temp = ''.join(card.xpath('td[2]/text()'))
			skill = re.search('.*技能位：(\d*).*卡片品质：(\d*)', temp).group(1)
			quality = re.search('.*技能位：(\d*).*卡片品质：(\d*)', temp).group(2)
			cardId = ''.join(card.xpath('td[1]/div/a/@href'))
			cardId = re.search('.*cardid=(.*)&.*', cardId).group(1)
			cardList.append({
				"level": int(level),
				"skill": int(skill),
				"quality": int(quality),
				"cardid": cardId
			})
		self.log.info('--获取现有卡片信息结束--')
		return cardList

	def deleteCard(self, cardId):
		deleteUrl = self.__CARD_PAGE + '?card=del&safeid=' + self.safeid + '&cardid=' + cardId
		res = self.req.get(deleteUrl)

	def getCard(self):
		self.log.info('--开始领取卡片--')
		cardList = self.getNowCard()
		sm = self.user.getSM()
		if len(cardList) == 3:
			minCardId = None
			minCardVal = sys.maxsize
			hopeLevel = sm * 2 + 30
			hopeSkill = 4
			hopeQuality = 8
			for card in cardList:
				val = int((card['level']/hopeLevel + card['skill']/hopeLevel + card['quality']/hopeQuality) * 1000)
				if val < minCardVal:
					minCardVal = val
					minCardId = card['cardid']
			self.deleteCard(minCardId)
		growupUrl = self.__CARD_PAGE + '?card=new&safeid=' + self.safeid
		res = self.req.get(growupUrl)
		self.log.info('--领取卡片结束--')
		self.log.info()