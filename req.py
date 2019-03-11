# -*- coding: UTF-8 -*-
import requests
import traceback

class KfReq:

	def __init__(self):
		self.headers = {
			'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
		}
		self.cookies = dict()

	def get(self, url, **kwargs):
		kwargs['method'] = 'GET'
		kwargs['url'] = url
		return self.request(**kwargs)

	def post(self, url, **kwargs):
		kwargs['method'] = 'POST'
		kwargs['url'] = url
		return self.request(**kwargs)

	def put(self, url, **kwargs):
		kwargs['method'] = 'PUT'
		kwargs['url'] = url
		return self.request(**kwargs)

	def delete(self, url, **kwargs):
		kwargs['method'] = 'DELETE'
		kwargs['url'] = url
		return self.request(**kwargs)

	def head(self, url, **kwargs):
		kwargs['method'] = 'HEAD'
		kwargs['url'] = url
		return self.request(**kwargs)

	def options(self, url, **kwargs):
		kwargs['method'] = 'OPTIONS'
		kwargs['url'] = url
		return self.request(**kwargs)

	def request(self, method, url, **kwargs):

		try:
			r = requests.request(method, url, headers=self.headers, cookies=self.cookies, verify=False, timeout=30, **kwargs)
			self.cookies.update(r.cookies.get_dict())
			return r.text
		except:
			traceback.print_exc()
			return self.request(method, url, **kwargs)
		