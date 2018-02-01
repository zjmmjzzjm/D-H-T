#!/bin/bash

for f in backup/*.csv; 
do
 echo $f
 python csv_hash_to_mysql.py $f
done
