# /usr/bin/env python
#
#
# config.json structure:
# {
# "uid": {
#			"access_token":"your_token"
#		}
#	}
# access_token you can get by following oaut_link below
#
# alternatively you can use make_config.py
#

import requests
import logging
import json
from time import sleep
from consts import oauth_link, api_version

#print(oauth_link)

from enum import Enum

#add error codes here for more obvious code
class ErrorCode(Enum):
	MuchRequestsError = 6


logger = logging.getLogger('warning')
logger.setLevel(logging.ERROR)


class VK:
	__api_url = "https://api.vk.com/method/"
	#in config file you have ids & access tokens
	__config_file = 'config.json'
	__config_data = None
	__timeout = 1
	__retries = 3

	def __init__(self, uid=None):
		if not self.__config_data:
			self.__config_data = json.load(open(self.__config_file))
		use_default = not uid
		if uid and not self.__config_data.get(uid, None):
			logger.warning("Couldn't find uid '{0}' in config file '{1}'".format(uid, self.__config_file))
			logger.warning("You should add access_token to config file to use this uid")
			use_default = True
		if use_default:
			uids = list(self.__config_data.keys())
			logger.warning("Using defaul uid")
			if len(uids) == 0:
				logger.error("No available uids, please add some to '{0}'".format(self.__config_file))
				exit(1)
			else:
				self.uid = uids[0]
		else:
			self.uid = uid
		self.__access_token = self.__config_data[self.uid]['access_token']

	def _get(self, url, params):
		resp = None
		retries = 0
		while (not resp and retries < self.__retries):
			try:
				resp = requests.get(url, params=params, timeout=self.__timeout)
			except requests.exceptions.Timeout:
				sleep(self.__timeout)
			retries += 1
		return resp

	def call_method(self, method, params):
		req_url = self.__api_url + '/' + method
		params = params.copy()
		params['access_token'] = self.__access_token
		params['v'] = api_version
		for _ in range(self.__retries):
			resp = self._get(req_url, params)
			if (not resp):
				logger.error("Something gone wrong!")
				logger.error('There are no response!')
				exit(1)

			resp.raise_for_status()
			parsed = json.loads(resp.text)
			if 'response' in parsed.keys():
				return parsed['response']
			elif parsed['error']['error_code'] == ErrorCode.MuchRequestsError:
				sleep(self.__timeout)
				continue
			else:
				logger.error("Something gone wrong!")
				logger.error(resp.text)
				exit(1)

#small testing
if __name__ == '__main__':
	vk = VK()

	# get subscriptions
	params = {'user_id': vk.uid}
	subscriptions = vk.call_method('users.getSubscriptions', params)
	print(subscriptions)
