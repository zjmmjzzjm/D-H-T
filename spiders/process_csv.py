#encoding: utf-8
import os
import csv


if __name__ == "__main__":
	import sys
	csvdir = sys.argv[1]
	container = set()
	outf = open(sys.argv[2], "w")
	writer = csv.writer(outf)
	dupnum = 0
	totalnum = 0
	csv.field_size_limit(1024*1024*100)
	for root, sub, fs in os.walk(csvdir):
		for f in fs:
			if(not f.endswith(".csv")):
				continue
			fullpath = root + "/" + f
			fh = open(fullpath, "r")
			reader = csv.reader(fh)
			print fullpath
			try:
				for infos in reader:
					try:
						totalnum += 1
						hashinfo = infos[0]
						content = infos[1]
						mag = infos[2]
						if(hashinfo in container):
							dupnum += 1
							continue
						container.add(hashinfo)
						writer.writerow(infos)

						#print mag 
					except Exception,e:
						print e
						print "fullpath: ", fullpath
						print infos
						#sys.exit(0)
				print "total num ", totalnum, " dupnum ", dupnum, " dup rate ", float(dupnum)/totalnum, " effective num ", totalnum - dupnum
			except Exception, e:
				print e


			fh.close()

	outf.close()

	print "total num ", totalnum, " dupnum ", dupnum, " dup rate ", float(dupnum)/totalnum, " effective num ", totalnum - dupnum

