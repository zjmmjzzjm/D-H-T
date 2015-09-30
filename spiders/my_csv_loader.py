#encoding: utf-8
import os
import csv

class my_csv_loader(object):
	
	def __init__(self, csv_file_name):
		self.filename  = csv_file_name
		self.filehandle = open(self.filename, 'r') 
		self.reader = csv.reader(self.filehandle)

	def load(self):
		infos = self.reader.next()
		hashinfo = infos[0]
		content = infos[1]
		mag = infos[2]
		yield hashinfo, content, mag
	
	def cleanup(self):
		if self.filehandle != None:
			self.filehandle.close()
			self.filehandle = None
		self.reader = None

if __name__ == "__main__":
	import sys
	ld = my_csv_loader(sys.argv[1])
	index = 0
	while True:
		try:
			hashinfo, content, mag = ld.load().next()
			print index, hashinfo, content, mag
			index += 1
		except Exception,e:
			print "Load Finish",e
			break




