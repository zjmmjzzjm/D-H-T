#encoding: utf-8
import os
import csv

class my_csv_storer(object):
	
	def __init__(self, csv_file_name):
		self.filename  = csv_file_name
		self.filehandle = open(self.filename, 'a') 
		self.writer = csv.writer(self.filehandle)

	def store(self, info_hash, content, magnet):
		self.writer.writerow([info_hash, content, magnet])
	
	def cleanup(self):
		if self.filehandle != None:
			self.filehandle.close()
			self.filehandle = None
		self.writer = None


