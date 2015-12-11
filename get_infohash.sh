#/bin/bash

if [ $1"x" != "x" ];
then
	echo "set days"
	((days=$1+1))
else
	days=8
fi
dt=`date +%Y%m%d`
cd download
mkdir $dt
cd $dt
cur=`date +%s`

echo $days

cmd="sftp root@128.199.121.74 <<H\ncd dht-work/dht-test/infohash/"
echo $cur
for((i=1; i<$days; i++))
do
	((d=$cur-$i*86400))

	dd=`date +%Y%m%d -d @$d` 
	cmd="$cmd\n get ${dd}_test"
done
cmd="$cmd \nH"
echo -e $cmd > tmp.sh
chmod +x tmp.sh
./tmp.sh


