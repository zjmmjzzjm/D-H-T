#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
cd $basepath
yesterday=`date -d 'yesterday' +%Y%m%d`
#file=${yesterday}_test 
#scp root@128.199.121.74:/root/dht-work/dht-test/infohash/$file download/$file
#head  -1000 download/$file > download/test.txt
#mv download/test.txt download/$file
#python download_torrent.py download/$file
file=${yesterday}_meta
#scp -r root@128.199.121.74:/root/dht-work/dht-test/metadata/$file torrents/
python parse_torrent.py torrents/$file/
csv_file=`echo torrents/${file}_magnet.csv | sed 's#/#_#g'`
scp $csv_file root@www.btmilk.com:/root/Workspace/data/
ssh root@www.btmilk.com "/root/Workspace/dht/auto_index.sh /root/Workspace/data/$csv_file >> /root/Workspace/data/auto.log 2>&1 &"

