import csv

import sys
csv.field_size_limit(int(1024*1024*1024))
f = open(sys.argv[1])
r = csv.reader(f)
for row in r:
	print row[0]

