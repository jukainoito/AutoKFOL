# -*- coding: UTF-8 -*-
from user import User
from req import KfReq
from log import Logging
from string import Template
from lxml import etree
import datetime
import re
import time

import constants

class Attacker(object):

	__LOOT_PAGE = constants.DOMAIN + '/kf_fw_ig_index.php'
	__ATTACK_PAGE = constants.DOMAIN + '/kf_fw_ig_intel.php'



	def __init__(self, user, log = None):
		self.safeid = user.safeid
		self.req = user.req
		if log is None:
			self.log = Logging(user.username)
		else:
			self.log = log
		self.attackTime = None

	def checkOnlineBattleIsOver(self, htmlTree=None):
		if htmlTree is None:
			res = self.req.get(self. __LOOT_PAGE)
			htmlTree = etree.HTML(res)
		pk_log = ''.join(htmlTree.xpath('//*[@id="pk_text"]/li/text()'))
		attacked = (pk_log == '今日战斗已完成，请重置后再战。')
		return attacked

	def checkOffLineBattleIsOver(self):
		if self.attackTime is None:
			return None
		attacked = (datetime.datetime.now().day - self.attackTime.day) == 0
		return attacked


	def checkAttacked(self):
		offLineBattleIsOver = self.checkOffLineBattleIsOver()
		self.log.info('检查线下争夺记录: ' + str(offLineBattleIsOver))
		if offLineBattleIsOver is None:
			onLineBattleIsOver = self.checkOnlineBattleIsOver()
			self.log.info('检查线上争夺记录: ' + str(onLineBattleIsOver))
			return onLineBattleIsOver
		else:
			return offLineBattleIsOver

	def getServerStatus(self, htmlTree):
		status = ''.join(htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[3]/table/tr[1]/td/span/text()'))
		return status[-2:]
	
	def attack(self):
		res = self.req.post(self.__ATTACK_PAGE, data=dict(safeid=self.safeid))
		return res

	def attackToEnd(self):
		stage = '0'
		while True:
			self.log.info('查询服务器状态')
			lootPage = self.req.get(self.__LOOT_PAGE)
			lootPageTree = etree.HTML(lootPage)
			serverStatus = self.getServerStatus(lootPageTree)
			self.log.info(serverStatus)
			if serverStatus == '空闲':
				self.log.info('开始争夺')
				attackRes = self.attack()
				#self.log.info(attackRes)
				if attackRes == 'no':
					break
				m = re.finditer(r'<li((?!</li>).)*</li>', attackRes)
				for s in m :
					tmp = ''.join(etree.HTML(s.group()).xpath('//text()'))
					if re.search('.*\s(\d*)\s层.*', tmp) != None:
						stage = re.search('.*\s(\d*)\s层.*', tmp).group(1)
					self.log.info(tmp)
				self.log.info()
				time.sleep(1)
			else:
				self.log.info('等待服务器状态变化...')
				time.sleep(60 * 5)
		return stage



	def autoAttack(self):
		self.log.info('--开始自动争夺--')
		self.log.info('检查是否已争夺')
		attacked = self.checkAttacked()
		stage = '0'
		if attacked:
			self.log.info('今日已进行争夺')
		else:
			stage = self.attackToEnd()
		self.log.info('--自动争夺结束--')
		self.log.info()
		self.attackTime = datetime.datetime.now()
		return stage

