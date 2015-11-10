#encoding: utf-8
import os
import csv


if __name__ == "__main__":
	import sys
	csvdir = sys.argv[1]
	container = set()
	outf = open(sys.argv[2], "a")
	writer = csv.writer(outf)
	dupnum = 0
	totalnum = 0
	for root, sub, fs in os.walk(csvdir):
		for f in fs:
			if(not f.endswith(".csv")):
				continue
			fullpath = root + "/" + f
			fh = open(fullpath, "r")
			reader = csv.reader(fh)
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
					writer.writerow([hashinfo, content, mag])

					#print mag 
				except Exception,e:
					print e
					print "fullpath: ", fullpath
					print infos
					#sys.exit(0)

			print fullpath
			print "total num ", totalnum, " dupnum ", dupnum, " dup rate ", float(dupnum)/totalnum, " effective num ", totalnum - dupnum
			fh.close()

	outf.close()

			print "total num ", totalnum, " dupnum ", dupnum, " dup rate ", float(dupnum)/totalnum, " effective num ", totalnum - dupnum

