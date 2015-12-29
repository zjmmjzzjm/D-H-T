#encoding: utf8
import re
import sys
import requests
from bs4 import BeautifulSoup
import my_csv_storer
import time
import os
import traceback
import socket
import random
import csv


class btdepot_craw(object):
	_headers = {'Connection': "keep-alive",
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
			'Host': 'www.btbook.com',
			'Cache-Control':"max-age=0",
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'Upgrade-Insecure-Requests':'1',
			}

	_headers1 = {'Connection': "keep-alive",
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
			'Host': 'www.btbook.com',
			"Referer":'http://www.btbook.com/',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'zh-CN,zh;q=0.8',
			'Upgrade-Insecure-Requests':'1',
			}
	_btdepot_url = "http://www.btbook.com"
	_referer = ""
	_csv_dir = "csv"
	_base_result = ""
        _csv_file = ""
        _csv_writer = ""
	def __init__(self, suffix = ""):
		if os.path.isdir(self._csv_dir) == False:
			os.mkdir(self._csv_dir)
		self.cur_key_seachcount = 0
		self.cur_key = ""
		self.pid = str(os.getpid())
		self.record_file = "btbook_record_" + suffix + "_"  + self.pid + ".txt"
		self._base_result = requests.get("http://www.btbook.com", headers=self._headers)
		url = "http://www.btbook.com/search/"+str(random.randint(1,10000)) +"/"
		self._referer = url
		self._base_result = requests.get(url, headers = self._headers1, cookies=self._base_result.cookies)
		self._headers['Referer'] = url
                self._csv_file = open("btbook_all.csv", "w")
                self._csv_writer = csv.writer(self._csv_file)



	def craw(self, keyword_list):
		pass
	def craw_single_keyword(self, keyword):
		self.cur_key = keyword
		#	time.sleep(4)
		self.cur_key_seachcount = 0
		search_url = self._btdepot_url + "/h/"+ str(keyword)
                r0 = requests.get(search_url, headers = self._headers, timeout=10, cookies=self._base_result.cookies)
                #print r0.cookies
                soup = BeautifulSoup(r0.content)
                bodys=soup.find_all('div', class_='panel-body')
                detail_header_bg=soup.find_all('tr', class_ = 'detail-header-bg')
                mag = bodys[0].a.string
                infohash=mag[20:60]
                filecount=detail_header_bg[1].contents[7].string.strip()
                contents = [ bodys[1].ol.contents[2*i + 1]  for i in range(int(filecount)) ]
                contents1 = [ c.contents[0] + " " + c.span.string.replace(u"\xa0", u"")  for c in contents ]
                contents2 = '\n'.join(contents1)
                title = soup.find_all('h4')[0].string
                contents3 = title + "\n" + contents2
                totalsize=detail_header_bg[1].contents[5].string.strip().replace(u'\xa0', u"")
                index_time = int(time.time())
                row = (unicode(infohash).encode('utf8'),unicode(contents3).encode('utf8'), unicode(totalsize).encode('utf8'),  index_time - random.randint(0, 60*24*3600) )
                self._csv_writer.writerow(row)
                self._csv_file.flush()
                print unicode(infohash).encode("utf8"), unicode(title ).encode('utf8')

if "__main__"== __name__:
	c = btdepot_craw(os.path.basename(sys.argv[1]).split('.')[0])

	socket.setdefaulttimeout(10)
	index = 1795500 
	while True:
		index  += 1
		keyword = str(index)
		print "key word: __" + keyword + "__" + " index : ", index

		try:
			c.craw_single_keyword(keyword)
			with open(c.record_file, "a") as frecord:
				frecord.write(str(index) + ", ok," + str(c.cur_key_seachcount) + ",  keyword : " + keyword + "\n")
		except Exception, e:
			with open(c.record_file, "a") as frecord:
				frecord.write(str(index) + ", fail, " + str(c.cur_key_seachcount) +",  keyword : " + keyword + "\n")
			print "Found Exception", e
			traceback.print_exc()


