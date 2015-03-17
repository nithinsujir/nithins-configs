#!/bin/bash
set -e
set -x

FAIL=0
KT='/home/nsujir/kernel-trees'

for d in `ls $KT`
do
	rm -rf /tmp/tg3-$d/
	mkdir -p /tmp/tg3-$d
	make clean
	cp *.c /tmp/tg3-$d
	cp *.h /tmp/tg3-$d
	cp Makefile /tmp/tg3-$d
	cp makeflags.sh /tmp/tg3-$d
	BCMCFGDIR=$KT/$d BCMSRCDIR=$KT/$d make -C /tmp/tg3-$d &
done

for job in `jobs -p`
do
	echo $job
	wait $job || let "FAIL+=1"
done

echo $FAIL

if [ "$FAIL" == "0" ];
then
	echo "Builds passed"
else
	echo "FAIL! ($FAIL)"
fi

make clean

