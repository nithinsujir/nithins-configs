#!/bin/bash
set -e
#set -x

if [ "x$1" == "x" ]
then
	echo "$0 <destdir> <file>"
	exit 1
fi

if [ "x$2" == "x" ]
then
	echo "$0 <destdir> <file>"
	exit 1
fi

if mount | grep -q "type nfs"
then
	echo "nfs mounted"
else
	echo "mounting nfs share"
	sudo mount -t nfs 172.16.50.201:/home/nsujir/share /media/nfs
fi

NFSDIR='/media/nfs'
DESTDIR=$NFSDIR/$1
FILE=$2

mkdir -p $DESTDIR

for ((i=1; i<9999; i++))
do
	echo
	echo "-----------Iteration $i"
	rm -f $DESTDIR/*

	date
	echo "Copying $FILE to $DESTDIR"
	cp $FILE $DESTDIR

	date
	echo "Calculating md5sum"
	md5=`md5sum $DESTDIR/$FILE | awk {'print $1'}`

	if [ "$md5.big" == "$FILE" ]
	then
		echo "Success!"
	else
		echo "Failed! md5 is $md5"
		exit 1
	fi
done

