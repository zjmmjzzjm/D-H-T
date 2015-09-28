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


class btdepot_craw(object):
	_headers = {'Connection': "keep-alive",
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
			'Referer': 'http://www.btdepot.com/',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6'
			}

	_headers1 = {'Connection': "keep-alive",
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36',
			'Cache-Control': 'max-age=0',
			'Host': 'www.btdepot.com',
			'Accept-Encoding': 'gzip, deflate, sdch',
			'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6',

			}
	_btdepot_url = "http://www.breadsearch.com"
	_csv_dir = "csv"
	def __init__(self):
		if os.path.isdir(self._csv_dir) == False:
			os.mkdir(self._csv_dir)
		self.cur_key_seachcount = 0
		self.cur_key = ""


	def craw(self, keyword_list):
		pass
	def craw_single_keyword(self, keyword):
		self.cur_key = keyword
		self.cur_key_seachcount = 0
		search_url = self._btdepot_url + "/search/" + keyword
		r = requests.get(search_url, headers = self._headers, timeout=10)
		#print r.cookies
		soup = BeautifulSoup(r.content)
		ret = re.search(r'totalPages: \d*',r.content)
		print "match result ", ret
		if ret is None:
			print r.content
		totalPages = int(ret.group(0).split(':')[1].strip())
		csv_name = self._csv_dir + "/breadsearch_" + time.strftime("%Y%m%d") + ".csv"
		storer = my_csv_storer.my_csv_storer(csv_name)
		print 'totalPages:',totalPages

		for page in range(1,totalPages + 1):
			try:
				search_url = self._btdepot_url + "/search/" + keyword +"/" + str(page)
				r = requests.get(search_url, headers = self._headers, timeout=10)
				#print r.cookies
				soup = BeautifulSoup(r.content)
				item_list = soup.find_all("div", class_ = "item_container")
				for i in range(len(item_list)):
					if(i == 0):
						continue
					temp = item_list[i].a["href"]
					#print "===>",i, "  " , temp 
					info_url = self._btdepot_url + temp
					r = requests.get(info_url, headers = self._headers1, cookies = r.cookies, timeout=10)
					child_soup = BeautifulSoup(r.content)
					magnet_url = child_soup.find_all("textarea" )[0].string
					print magnet_url
					size = child_soup.find_all("span", string="Size: ")[0].next_sibling.string
					files = child_soup.find_all("span", string="Files: ")[0].next_sibling.string
					index_date = child_soup.find_all("span", string="Index Date: ")[0].next_sibling.string
					hash_info  = child_soup.find_all("span", string="Hash: ")[0].next_sibling.string
					title = child_soup.find_all('h1', class_ = 'torrent_title')[0].string


					
					detailfiles = child_soup.find_all("div")
					files = []
					for d in detailfiles:
						if d.has_attr('style') and d['style'] == "margin-bottom: 50px;":
							fnn = d.find_all('div')
							files = [ '-'.join(e.find_all('span')[0].strings) + " " + e.find_all('span')[1].string for e in fnn]
					content = title + "\n" + "\n".join(files)
					#print '===============>'
					#print type(hash_info)
					#print type(content.encode('utf8'))
					#print type(magnet_url)
					#print '<==============='
					storer.store(unicode(hash_info).encode('utf8'), unicode(content).encode('utf8'), unicode(magnet_url).encode('utf8'))
					self.cur_key_seachcount += 1
			except Exception, e:
				print "found exception", e
				traceback.print_exc()

		storer.cleanup()

if "__main__"== __name__:
	c = btdepot_craw()
	f = open(sys.argv[1], "rb")

	socket.setdefaulttimeout(10)
	index = 0
	for l in f.readlines():
		keyword = l.strip()
		index  += 1
		print "key word: __" + keyword + "__" + " index : ", index

		try:
			c.craw_single_keyword(keyword)
			with open("breadSearchrecord.txt", "a") as frecord:
				frecord.write(str(index) + ", ok," + str(c.cur_key_seachcount) + ",  keyword : " + keyword + "\n")
		except Exception, e:
			with open("breadSearchrecord.txt", "a") as frecord:
				frecord.write(str(index) + ", fail, " + str(c.cur_key_seachcount) +",  keyword : " + keyword + "\n")
			print "Found Exception", e
			traceback.print_exc()

