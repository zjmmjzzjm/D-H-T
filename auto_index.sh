#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
cd $basepath
python csv_to_mysql.py $1
/usr/local/coreseek/bin/indexer delta --rotate
/usr/local/coreseek/bin/indexer --merge main delta --rotate
python mysql.py -u

