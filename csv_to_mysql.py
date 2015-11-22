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
        infohash = row[0]
        content = row[1]
        size = row[2]
        t = row[3]
        mysql_handler.insert_info(infohash, content, size, t)
        i += 1
        if i % 100 == 0:
            print "insert ", i, " rows "


