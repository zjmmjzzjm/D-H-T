import re
import requests
from bs4 import BeautifulSoup

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
	_btdepot_url = "http://www.btdepot.com"
	def __init__(self):
		pass
	def craw(self, keyword_list):
		pass
	def craw_single_keyword(self, keyword):
		search_url = self._btdepot_url + "/search/" + keyword
		r = requests.get(search_url, headers = self._headers)
		#print r.cookies
		soup = BeautifulSoup(r.content)
		ret = re.search(r'totalPages: \d*',r.content)
		totalPages = int(ret.group(0).split(':')[1].strip())
		print 'totalPages:',totalPages
		for page in range(1,totalPages + 1):
			search_url = self._btdepot_url + "/search/" + keyword +"/" + str(page)
			r = requests.get(search_url, headers = self._headers)
			#print r.cookies
			soup = BeautifulSoup(r.content)
			item_list = soup.find_all("div", class_ = "item_container")
			for i in range(len(item_list)):
				if(i > 0):
					temp = item_list[i].a["href"]
					print "===>",i, "  " , temp 
					info_url = self._btdepot_url + temp
					r = requests.get(info_url, headers = self._headers1, cookies = r.cookies)
					child_soup = BeautifulSoup(r.content)
					magnet_url = child_soup.find_all("textarea" )[0].string
					print 'magnet : ', magnet_url
					size = child_soup.find_all("span", string="Size: ")[0].next_sibling.string
					files = child_soup.find_all("span", string="Files: ")[0].next_sibling.string
					index_date = child_soup.find_all("span", string="Index Date: ")[0].next_sibling.string
					hash_info  = child_soup.find_all("span", string="Hash: ")[0].next_sibling.string
					
					detailfiles = child_soup.find_all("div")
					for d in detailfiles:
						if d.has_attr('style') and d['style'] == "margin-bottom: 50px;":
							fnn = d.find_all('div')
							for e in fnn:
								filename = '-'.join(e.find_all('span')[0].strings)
								size = e.find_all('span')[1].string
								print  "file:", filename, "===>size:", size

					print "size : ", size , " files: " , files, " index_date " , index_date, "hash info " , hash_info
			

		

if "__main__"== __name__:
	c = btdepot_craw()
	c.craw_single_keyword("byd")

