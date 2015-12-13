# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import base64
import time
import csv
import random

import socket
class cilisou_craw(object):
	cilisou_url =  "http://www.cilisou.cn/s.php"
	def __init__(self):
		self.soup = ""

	def craw(self, keyword_list):
		pass

	def craw_single_keyword(self, keyword):
		start_page = 1
		search_url = self.cilisou_url + "?q=" + keyword 
		print search_url
		self.soup = self.get_soup(search_url)
		end_page = self.get_page_count()

		print "end page ", end_page
		current_page = start_page
		while current_page <= end_page:
			search_url = self.cilisou_url + "?q=" + keyword  + "&p=" + str((current_page - 1))
			r = requests.get(search_url)
			soup = BeautifulSoup(r.content)

			magnet_list = soup.find_all("table", class_ = "torrent_name_tbl")
			for i in range(len(magnet_list)):
				if i % 2 == 0:
					continue
				tag = magnet_list[i]
				magnet_url = tag.tr.td.a["href"]
				files = tag.parent.find_all("pre")
				tmp = (re.sub("<br>", "\n", str(files[0])))
				tmp = re.sub(r'<[^>]*>', "", tmp)
				files = tmp
				#总大小.
				tmptag = tag.tr.td.next_sibling.next_sibling
				size = tmptag.find_all("span", class_ = "attr_val")[0].string.strip()

				# 文件数量.
				tmptag = tmptag.next_sibling.next_sibling
				file_cout = tmptag.find_all("span", class_ = "attr_val")[0].string.strip()
				#下载数.
				tmptag = tmptag.next_sibling.next_sibling
				#添加时间.
				tmptag = tmptag.next_sibling.next_sibling
				add_time = tmptag.find_all("span", class_ = "attr_val")[0].string.strip()
				#发现时间》
				tmptag = tmptag.next_sibling.next_sibling
				find_time = tmptag.find_all("span", class_ = "attr_val")[0].string.strip()
				print "magnet url : " , magnet_url
				print "文件数量", file_cout, " 总大小 ", size, " 添加时间 ", add_time, " 发现时间: " , find_time
				print "文件列表: ", files
			time.sleep(0.5)
			current_page += 1



			


	def get_page_count(self):
		page = self.soup.find_all("table", class_ = "pager")
		return  int(page[0].tr.contents[3].string.strip().split("/")[1])

	def get_soup(self, search_url):
		r = requests.get(search_url)
		self.soup = BeautifulSoup(r.content)
		return self.soup

def craw_all():
	baseurl = "http://www.cilisou.cn/info.php"
	i = 69123 
	csvfile = open('clisouall.csv', 'w')
	writer = csv.writer(csvfile)
	while True:
		url = baseurl+ '?sphinx_id=' + str(i)+'&info_hash='+str(i)
		i += 1
		try:
			r = requests.get(url, timeout =20)
			soup = BeautifulSoup(r.content)
			s1 = soup.find_all("table", class_ = "torrent_info_tbl")[0]
			mag=s1.contents[3].contents[3].a['href']
			title=s1.contents[5].contents[3].string
			totalsize=s1.contents[9].contents[3].string
			count=s1.contents[15].contents[3].string
			count = int(count)
			fileinfos = []
			for fn in range(count):
				fi = s1.contents[20 + 2*fn + 1].contents[3].string + " " + s1.contents[20 + 2*fn + 1].contents[1].string.replace(" ", "")
				fileinfos.append(fi)

			contents = title + '\n' + '\n'.join(fileinfos)
			
			infohash = mag[20:60]
			index_time = int(time.time())
			row = (unicode(infohash).encode('utf8'),unicode(contents).encode('utf8'), unicode(totalsize).encode('utf8'),  index_time - random.randint(0, 60*24*3600) )
			writer.writerow(row)
#                        time.sleep(1)

			print i, ": " ,mag
		except Exception,e:
			print "found exception, ", e

	csvfile.close()







if __name__ == "__main__":
	socket.setdefaulttimeout(10)
#	crawler = cilisou_craw()
#	crawler.craw_single_keyword("咒怨")
	craw_all()
