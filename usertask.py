# -*- coding: UTF-8 -*-
from user import User
from attack import Attacker
from box import Box
from equip import Equip
from item import Item
from shop import Shop
from growup import Growup
from card import Card
from req import KfReq
from log import Logging

import time
import datetime


class UserTask(object):

	run = True

	def __init__(self, username, password, 
		openBoxType=[True, True, True, True], 
		smeltEquipType=[True, True, True, False], 
		useItemType=[True, True, True, True, True, True], 
		sellItemType=[True, True, True, True, True, True],
		buyExp=True, log=None):
		self.username = username
		self.password = password
		self.openBoxType = openBoxType
		self.smeltEquipType = smeltEquipType
		self.useItemType = useItemType
		self.sellItemType = sellItemType
		if log is None or len(logfilePath)==0:
			self.log = Logging(self.username)
		else:
			self.log = log
		self.buyExp = buyExp

	def init(self):
		self.user = User(self.username, self.password)
		self.user.login()
		self.attacker = Attacker(self.user, log = self.log)
		self.box = Box(self.user, self.openBoxType)
		self.equip = Equip(self.user, self.smeltEquipType)
		self.item = Item(self.user, self.useItemType, self.sellItemType)
		self.shop = Shop(self.user)
		self.growup = Growup(self.user)
		self.card = Card(self.user)

	def task(self):
		while self.run:
			while self.attacker.autoAttack() is not True:
				self.run = False
				break
				# self.log.info('睡眠到明日0点...')
				# today = datetime.date.today()
				# tomorrow = today + datetime.timedelta(days=1)
				# tomorrowTimestamp = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
				# nowTimestamp = int(time.time())
				# time.sleep(tomorrowTimestamp-nowTimestamp+1)
			self.box.autoOpenBox()
			self.equip.autoSmelt()
			self.item.autoItemCommand()
			if self.buyExp is True:
				self.shop.autoBuy()
			self.growup.growup()
			self.card.getCard()
			self.log.info('============= END USER TASK ================')
			break
