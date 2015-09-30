#encoding:utf-8
import os
import requests
import string
import re
import traceback
import urlparse
from bs4 import BeautifulSoup

class Star_names_crawler(object):
	__url = 'http://www.manmankan.com/dy2013/mingxing/'
	def __init__(self):
		pass
	def get_names(self):
		for letter in  string.ascii_uppercase:
			try:
				first_url = urlparse.urljoin(self.__url, letter)
				print "first_url: ", first_url
				res = requests.get(first_url, timeout = 10)
				soup =  BeautifulSoup(res.content)
				s1 = soup.find_all('div', class_ = 'i_cont')
				s2 = s1[0].find_all('a', target='_blank')
				names = [n.string for n in s2]
				self.save_names(names)

				s4 = re.findall('index_\d\.shtml', res.content)
				if len(s4) == 0 :
					continue
				del s4[len(s4) - 1]
				for page in s4:
					try : 
						next_url = urlparse.urljoin(first_url, page)
						print "next_url:", next_url
						res = requests.get(first_url, timeout = 10)
						soup =  BeautifulSoup(res.content)
						s1 = soup.find_all('div', class_ = 'i_cont')
						s2 = s1[0].find_all('a', target='_blank')
						names = [n.string for n in s2]
						self.save_names(names)
					except Exception, ee:
						print "Exception ", ee
						traceback.print_exc()
			except Exception, e:
				print "exception :", e
				traceback.print_exc()

	def save_names(self, name_list):
		with open("manmankan_stars.txt", 'a') as f:
			for name in name_list:
				f.write(name.encode("utf8") + "\n")




if __name__ == "__main__":
	crawler = Star_names_crawler()
	crawler.get_names()
