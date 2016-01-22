#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
cd $basepath
python csv_to_msyql.py $1
/usr/local/coreseek/csft/bin/indexer delta --rotate
/usr/local/coreseek/csft/bin/indexer –merge main delta --rotate

