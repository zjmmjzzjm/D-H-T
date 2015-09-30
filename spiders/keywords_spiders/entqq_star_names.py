#encoding:utf-8
import os
import requests
import string
import re
import traceback
import urlparse
from bs4 import BeautifulSoup

class Star_names_crawler(object):
	__url = 'http://ent.qq.com/c/all_star.shtml'
	def __init__(self):
		pass
	def get_names(self):
		try:
			res = requests.get(self.__url)
			soup = BeautifulSoup(res.content)
			links = soup.find_all('a', target='_blank')
			names = [n.string for n in links if n.string]
			self.save_names(names)
		except Exception, e:
			print "exception :", e
			traceback.print_exc()

	def save_names(self, name_list):
		with open("qq_stars.txt", 'a') as f:
			for name in name_list:
				f.write(name.encode("utf8") + "\n")




if __name__ == "__main__":
	crawler = Star_names_crawler()
	crawler.get_names()

