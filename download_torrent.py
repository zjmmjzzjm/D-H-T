import os
import sys
import shutil
import time
import json
import random
import traceback as tb
import tempfile
import urllib2
import urllib
import threading


def _download_call_back(blocknum, blocksize, totalsize):
	percent = 100 * blocknum * blocksize / totalsize
	print '%.2f%%, total %d ' % (percent , totalsize)
class TorrentDownloader(object):
	_thunder_url = "http://bt.box.n0808.com"
	torrent_dir = "torrents"
	def __init__(self):
		pass

	def download_from_thunder(self,info_hash):
		info_hash = info_hash.upper()
		url = self._thunder_url + '/' + info_hash[0:2] + '/' + info_hash[-2:None] + '/' +info_hash + '.torrent'
		print "downloading: " + url
		filename = self.torrent_dir + '/'  + info_hash + '.torrent'
		ret = urllib.urlretrieve(url,filename, _download_call_back)
		size = os.path.getsize(filename)
		if(size < 300):
			os.remove(filename)
			print "download " + filename + " Failed."
		else:
			print 'download ' + filename + " OK."
		pass


	def download_from_btdepot(self,info_hash):
		pass

def download_thread(index, info_hash_list):
	downloader = TorrentDownloader()
	print "Thread " + str(index) + " started "
	for info_hash in info_hash_list:
		downloader.download_from_thunder(info_hash)
	
	print "Thread " + str(index) + " stopped"


if __name__ == '__main__':

	if(len(sys.argv) < 2):
		print 'Usage : download_torrent.py info_hash_list'
		sys.exit(-1)

	if not os.path.exists(TorrentDownloader.torrent_dir):
		os.mkdir(TorrentDownloader.torrent_dir)
	info_hash_file = open(sys.argv[1])
	info_hash_list = [l.strip() for l in info_hash_file.readlines()]
	info_hash_file.close()
	
	for l in info_hash_list:
		print "info_hash: " + l + " len " + str(len(l))

	max_treads = 5
	group_size = len(info_hash_list) / max_treads
	print "group_size " + str(group_size)
	pass
		
	threads = []
	for i in range(max_treads):
		t = threading.Thread(target=download_thread, args=(i,info_hash_list[i * group_size : (i+1)*group_size]))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()	
	
	pass