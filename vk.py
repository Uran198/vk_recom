#/usr/bin/env python
#
#
# config.json structure:
#	{
#		"uid": {
#			"access_token":"your_token"
#		}
#	}
# access_token you can get by following oaut_link below
#
# alternatively you can use make_config.py
#

import requests
import logging
from time import sleep
from operator import itemgetter
import os
import json
from consts import oauth_link

print(oauth_link)

logger = logging.getLogger('warning')
logger.setLevel(logging.WARNING)

class VK:
	__api_url = "https://api.vk.com/method/"
	#in config file you have ids & access tokens
	__config_file = 'config.json'
	__config_data = None

	def __init__(self, uid=None):
		if not self.__config_data:
			self.__config_data = json.load(open(self.__config_file))
		if uid and self.__config_data.get(uid, None):
			self.__access_token = self.__config_data[uid]['access_token']
		else:
			if not self.__config_data.get(uid, None):
				logger.warning("Couldn't find uid '{0}' in config file '{1}'".format(uid, self.__config_file))
				logger.warning("You should add access_token to config file to use this uid")
				logger.warning("You can do it by following the link:")
				logger.warning(oath_link)
			self.__access_token = ''

	def call_method(self, method, params):
		req_url = self.__api_url+'/'+method
		params = params.copy()
		params['access_token'] = self.__access_token
		return requests.get(req_url, params=params)

params = {}
vk = VK(uid = "171937039")
resp = vk.call_method('fave.getPosts', params)
resp.raise_for_status()
data = json.loads(resp.text)
print(data)
