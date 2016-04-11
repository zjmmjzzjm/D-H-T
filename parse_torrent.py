import libtorrent as lt
import time
import os

import sys
import mysql

import csv

def parse_torrent(torrent_name, is_debug = False):
	stat = os.stat(torrent_name)
	index_time = int(stat.st_ctime)
	e = lt.bdecode(open(torrent_name, 'rb').read())
	info = lt.torrent_info(e)
	total_size = 0
	content = info.name() + "\n"
	num_file = info.num_files()

	if is_debug:
		print "num_file " + str(num_file)
	for i in range(num_file):
		f = info.file_at(i)
		content += f.path + " " + str(f.size) + "\n"
		total_size += f.size
		infohash = info.info_hash().to_string().encode("HEX")

	if is_debug:
		print "Name: " + info.name()
		print "info_hash: " ,  infohash
		print "num_files: ", num_file
		print "contents: " + content
		print " Total size: " , total_size
	return ( infohash, content, total_size, index_time )


def parse_and_insert(dirname = "torrents"):
	csv_name ='_'.join( dirname.split('/')) + "magnet.csv"
	fh = open(csv_name, "w")
	csv_writer = csv.writer(fh)
	total = 0
	print csv_name
	for root,dirs, files in os.walk(dirname):
		if len(files) == 0:
			continue
		for f in files:
			torrent_name = root + '/' + f;
			print torrent_name
			try:
				tinfo = parse_torrent(torrent_name, False) 
				csv_writer.writerow(tinfo)
				total += 1
				if total %  400 == 0:
					print total
			except Exception , e:
				print "cannot parse torrent " +  torrent_name , e
				pass

	fh.close()

	print total

if __name__ == "__main__":
		#parse_torrent(sys.argv[1], True)

		#sys.exit(0)
		begin_time = time.time()
		print "begin_time is ", begin_time
		parse_and_insert(sys.argv[1])
		end_time = time.time()
		print "begin_time is ", begin_time
		print "end_time is ", end_time
		print "total consume is ", end_time-begin_time

#pass
#params = { save_path: '.', \
#		storage_mode: lt.storage_mode_t.storage_mode_sparse, \
#		ti: info }
#h = ses.add_torrent(params)
#
#s = h.status()
#while (not s.is_seeding):
#	s = h.status()
#	state_str = ['queued', 'checking', 'downloading metadata', \
#	'downloading', 'finished', 'seeding', 'allocating']
#	print '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
#	(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
#	s.num_peers, state_str[s.state])
#	time.sleep(1)
