#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
cd $basepath
yesterday=`date -d 'yesterday' +%Y%m%d`
file=${yesterday}_test 
scp root@128.199.121.74:/root/dht-work/dht-test/infohash/$file download/$file
#head  -500 download/$file > download/test.txt
#mv download/test.txt download/$file
python download_torrent.py download/$file
python parse_torrent.py torrents/$file/
csv_file=`echo torrents/${file}_magnet.csv | sed 's#/#_#g'`
scp $csv_file root@www.btmilk.com:/root/Workspace/data/


