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
import socket 
import urllib2
import gzip


def _download_call_back(blocknum, blocksize, totalsize):
	percent = 100 * blocknum * blocksize / totalsize
	print '%.2f%%, total %d ' % (percent , totalsize)
class TorrentDownloader(object):
	_thunder_url = "http://bt.box.n0808.com"
	_torcache_url = "http://www.torcache.net"
	torrent_dir = "torrents"
	def __init__(self):
		pass

	def download_from_thunder(self,info_hash):
		try:
			info_hash = info_hash.upper()
			url = self._thunder_url + '/' + info_hash[0:2] + '/' + info_hash[-2:None] + '/' +info_hash + '.torrent'
			print "downloading from thunder: " + url
			filename = self.torrent_dir + '/'  + info_hash + '.torrent'
			if os.path.isfile(filename) : 
				print " file %s exists" % filename
				return 0
			ret = urllib.urlretrieve(url,filename, _download_call_back)
			size = os.path.getsize(filename)
			if(size < 300):
				os.remove(filename)
				print "download " + filename + " Failed."
				return -1
			else:
				print 'download ' + filename + " OK."
				return 0

		except Exception, e:
			print " down load except " + str(e)
			return -1
		finally:
			print " down load finish"

		return -1

	def download_from_btdepot(self,info_hash):
		pass

	def download_from_torcache(self, info_hash):
		try:
			info_hash = info_hash.upper()
			url = self._torcache_url + '/torrent/' +info_hash + '.torrent'
			print "downloading from torcache: " + url
			filename = self.torrent_dir + '/'  + info_hash + '.torrent'
			if os.path.isfile(filename) : 
				print " file %s exists" % filename
				return 0
			ret = urllib2.urlopen(url)
			try:
				f = open(filename, "w")
				f.write(ret.read())
				f.close()
				gzf = gzip.open(filename)
				c = gzf.read()
				gzf.close()
				f = open(filename, "w")
				f.write(c)
				f.close()

			except Exception, e:
				print "Write file failed." + filename
				return -1;
		except Exception, e:
			print " down load except " + str(e)
			return -1
		finally:
			print " down load finish"

		return -1

def download_thread(index, info_hash_list):
	downloader = TorrentDownloader()
	print "Thread " + str(index) + " started "
	for info_hash in info_hash_list:
		ret = -1
		ret = downloader.download_from_thunder(info_hash)
		if(ret != 0):
			ret = downloader.download_from_torcache(info_hash)
	
	print "Thread " + str(index) + " stopped"

def init_socket():
	socket.setdefaulttimeout(10)

if __name__ == '__main__':

	if(len(sys.argv) < 2):
		print 'Usage : download_torrent.py info_hash_list'
		sys.exit(-1)

        init_socket()
        names = os.path.basename(sys.argv[1])
        names = names.split(".")
        TorrentDownloader.torrent_dir = TorrentDownloader.torrent_dir +  "/" + names[0]

	if not os.path.exists(TorrentDownloader.torrent_dir):
		os.mkdir(TorrentDownloader.torrent_dir)
	info_hash_file = open(sys.argv[1])
	info_hash_list = [l.strip() for l in info_hash_file.readlines()]
	info_hash_file.close()
	
	#for l in info_hash_list:
		#print "info_hash: " + l + " len " + str(len(l))

	max_treads = 5
	group_size = len(info_hash_list) / max_treads
	print "group_size " + str(group_size)
		
	threads = []
	for i in range(max_treads):
		if( i < max_treads - 1 ):
			t = threading.Thread(target=download_thread, args=(i,info_hash_list[i * group_size : (i+1)*group_size]))
		else :
			t = threading.Thread(target=download_thread, args=(i,info_hash_list[i * group_size : ]))
		threads.append(t)
		t.start()

	for t in threads:
		t.join()	
	
