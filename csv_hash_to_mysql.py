import mysql

if __name__ == "__main__":
	import csv
	import sys
	csv.field_size_limit(1024*1024*100)
	csvfile = open(sys.argv[1])
	reader = csv.reader(csvfile)
	mysql_handler = mysql.Mysql_hanle()
	i = 0
	for row in reader:
		try:
			infohash = row[0]
			mysql_handler.insert_info_hash_set(infohash.upper())
			i += 1
			if i % 400 == 0:
				print "insert ", i, " rows "
		except Exception,e:
			print "exception : " + str(e)


