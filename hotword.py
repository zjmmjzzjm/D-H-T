#encoding: utf8
import re
import sys
import requests
from bs4 import BeautifulSoup
import time
import os
import traceback
import socket
import random
import csv
import mysql


class btdepot_craw(object):
	_btdepot_url = "http://www.btcherry.org"
	_referer = ""
	_csv_dir = "csv"
	_base_result = ""
	_csv_file = ""
	_csv_writer = ""
	def __init__(self, suffix = ""):
		if os.path.isdir(self._csv_dir) == False:
			os.mkdir(self._csv_dir)
		self.pid = str(os.getpid())
		self.record_file = "btbook_record_" + suffix + "_"  + self.pid + ".txt"
		self._mysql_handler = mysql.Mysql_hanle()

	def craw(self, keyword_list):
		pass
	def craw_single_keyword(self, keyword):
		self.cur_key = keyword
		search_url = 'http://btbt.tv/'
		r0 = requests.get(search_url)
		soup = BeautifulSoup(r0.content)
		hot = soup.find_all('ul',class_="hot_list")
		for h in hot:
			aa = h.find_all('a') 
			tp = h["id"].split("_")[1]
			li = [unicode(a.string).encode("utf8").replace("《", "").replace("》","") for a in aa]
			time.sleep(2)
			self._mysql_handler.update_hot_words(tp, li)
		return

if "__main__"== __name__:
	c = btdepot_craw()
	socket.setdefaulttimeout(10)
	try:
		c.craw_single_keyword("")
	except Exception, e:
		print "Found Exception", e
		traceback.print_exc()


