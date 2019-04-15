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

	abilityAbs = {
		'增加攻击力': 'ATK', 
		'增加暴击伤害': 'CRT', 
		'增加技能伤害': 'SKL', 
		'穿透对方意志': 'BRC', 
		'生命夺取': 'LCH', 
		'增加速度': 'SPD', 
		'攻击': 'ATK', 
		'暴击': 'CRT', 
		'技能': 'SKL', 
		'穿透': 'BRC', 
		'吸血': 'LCH', 
		'速度': 'SPD', 
		'被攻击回血100+': 'HEL', 
		'获得无护甲魔法盾500+': 'SLD', 
		'每减少5%生命值获得额外意志': 'AMR', 
		'反弹对方实际伤害15%+': 'RFL', 
		'减少来自暴击的伤害10%+': 'CRD', 
		'减少来自技能的伤害10%+': 'SRD', 
		'回血': 'HEL', 
		'护盾': 'SLD', 
		'加防': 'AMR', 
		'反伤': 'RFL', 
		'暴减': 'CRD', 
		'技减': 'SRD'
	}

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
		equipTable = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[5]/table/tr')
		
		equipList = []
		for equip in equipTable:
			equipId = ''.join(equip.xpath('td[1]/@id'))
			equipId = re.search('(\d*)$', equipId).group(1)
			if len(equipId) == 0:
				continue
			equidName = ''.join(equip.xpath('td[3]/span[1]/text()'))

			info = equip.xpath('td[3]/text()')
			# 是否存在神秘
			subAbList = []
			if info[1] == '。':
				smAbility = ''.join(equip.xpath('td[3]/span[2]/text()'))
				mainAbility = info[2]
				subAbList = info[3:]
			else:
				smAbility = ''
				mainAbility = info[1]
				subAbList = info[2:]
			subAbility = ''.join(subAbList)

			mainAbility = mainAbility.replace('主属性：', '').split('。')
			subAbility = subAbility.replace('从属性：', '').split('。')
			mainAbilityAb = []
			for ability in mainAbility:
				if len(ability) == 0:
					continue
				ab = re.search('(.*)\(.*\)', ability).group(1)
				mainAbilityAb.append(self.abilityAbs[ab])

			subAbilityAb = []
			for ability in subAbility:
				if len(ability) == 0:
					continue
				ab = re.search('([^(]*)\(.*\)', ability).group(1)
				subAbilityAb.append(self.abilityAbs[ab])

			subMissCount = 0
			for ab in subAbilityAb:
				if ab not in mainAbilityAb:
					subMissCount = subMissCount + 1

			equipList.append({
				"id": equipId,
				"name": equidName,
				"smAbility": smAbility,
				"hasSmAbility": smAbility != '',
				"mainAbility": mainAbilityAb,
				"subAbility": subAbilityAb,
				"subMiss": subMissCount
			})

		# equipIds = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[5]/table/tr/td[1]/@id')
		# equipNames = htmlTree.xpath('//*[@id="alldiv"]/div[4]/div[2]/div[5]/table/tr/td[3]/span[1]/text()')

		# equipList = []
		# for i in range(0, len(equipIds)):
		# 	equipList.append(dict(id=re.search('(\d*)$', equipIds[i]).group(1), name=equipNames[i]))
		
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
			print(equipList)
			for equip in equipList:
				if re.match(matchRegex, equip['name']) or (equip['hasSmAbility'] == False and equip['subMiss'] >= 2):
					self.smeltEquip(equip['id'])
					equipList.remove(equip)
					self.log.info('熔炼:\t' + equip['name'] + '\t' + equip['id'])

			if beforeSize == len(equipList):
				break
		self.log.info('--自动熔炼结束--')
		self.log.info()