# -*- coding: UTF-8 -*-
import threading
import sys
import os
import json
from usertask import UserTask

import argparse

from requests.structures import CaseInsensitiveDict

sys.path.append('.')

import warnings
warnings.filterwarnings('ignore')


parser = argparse.ArgumentParser()
parser.add_argument('config', nargs=1, help='json config file', metavar='json config file')
args = parser.parse_args()

CONFIG_FILE = os.path.realpath(args.config[0])

'''
config file template
[{
	"username": "用户名",
	"password": "密码",
	# 打开盒子类型, 普通 幸运 稀有 传奇
	"openBoxType": [true, true, true, true],
	# 熔炼盒子类型, 普通 幸运 稀有 传奇
	"smeltEquipType": [true, true, true, false],
	# 将会先判断是否使用，再判断出售
	# 使用道具类型, 0蕾米莉亚同人漫画,1十六夜同人漫画,2档案室钥匙,3傲娇LOLI娇蛮音CD,4消逝之药,5整形优惠卷
	"useItemType": [true, true, true, true, true, true],
	# 出售道具类型, 0蕾米莉亚同人漫画,1十六夜同人漫画,2档案室钥匙,3傲娇LOLI娇蛮音CD,4消逝之药,5整形优惠卷
	"sellItemType": [true, true, true, true, true, true],
	# 是否购买商店经验值
	"buyExp": true
}]
'''

def readConfig():
	try:
		if os.path.exists(CONFIG_FILE):
			with open(CONFIG_FILE, mode='r', encoding='utf-8') as f:
				data = json.load(f)
				return data
		else:
			return None
	except json.JSONDecodeError as e:
	    print('JSONDecodeError: ', e)

def dictRetVal(data, key):
    if data is None or key is None:
        return None
    d = CaseInsensitiveDict(data)
    return None if key not in d else d[key]



def runTask(usertask):
	usertask.task()

if __name__ == '__main__':
	config = readConfig()
	if config is None:
		print('error: config file is not found')
		sys.exit(1)
	if isinstance(config, dict):
		config = [config]

	threads = []
	for signleConfig in config:
		username = dictRetVal(signleConfig, 'username')
		password = dictRetVal(signleConfig, 'password')
		openBoxType = dictRetVal(signleConfig, 'openBoxType')
		smeltEquipType = dictRetVal(signleConfig, 'smeltEquipType')
		useItemType = dictRetVal(signleConfig, 'useItemType')
		sellItemType = dictRetVal(signleConfig, 'sellItemType')
		buyExp = dictRetVal(signleConfig, 'buyExp')
		if username is None or password is None:
			continue
		userTask = UserTask(username=username, password=password, 
			openBoxType=openBoxType, smeltEquipType=smeltEquipType, 
			useItemType=useItemType, sellItemType=sellItemType, buyExp=buyExp)
		userTask.init()
		threads.append(threading.Thread(target=runTask,args=(userTask,)))

	for t in threads:
	    t.setDaemon(True)
	    t.start()
	for t in threads:
	    t.join()