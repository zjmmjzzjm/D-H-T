#encoding: utf-8
import os
import csv
import time
import re
import random
def convert1(src, target):
	import csv
	csvfile = open(src,'r')
	reader = csv.reader(csvfile)
	savecsv_file = open(target, "w")
	writer = csv.writer(savecsv_file)
	for infos in reader:
		hashinfo = infos[0]
		content = infos[1]
		mag = infos[2]
		r=re.match('(magnet:\?xt=urn:btih:[^&]*)&xl=([^&]*)(.*)', mag)
		totalsize = -1
		try:
			totalsize = r.group(2) 
		except Exception,e:
			print e
		index_time = int(time.time())
		row = (hashinfo, content, totalsize, index_time - random.randint(0, 60*24*3600) )
		writer.writerow(row)
		print hashinfo, totalsize, index_time
		
	savecsv_file.close()
	csvfile.close()





if __name__ == "__main__":
	import sys

	src_csv = sys.argv[1]
	target_csv = sys.argv[2]
	convert1(src_csv, target_csv)


