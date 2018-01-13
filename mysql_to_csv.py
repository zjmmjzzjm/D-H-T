import mysql

if __name__ == "__main__":
    import csv
    import sys
    csv.field_size_limit(1024*1024*100)
    csvfile = open(sys.argv[1], 'w')
    writer = csv.writer(csvfile)
    mysql_handler = mysql.Mysql_hanle()
    for i in range(1,21000000):
        row = mysql_handler.select_hash_info(i)
        infohash = row[1]
        content = row[2]
        size = row[3]
        t = row[4]
        writer.writerow([infohash, content.encode('utf8'), size, t])
        if i % 300 == 0:
           print i
        #print row
        #print  infohash, size, t
        #break



