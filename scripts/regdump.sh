#!/bin/bash

if [ "x$1" == "x" ]
then
	echo "PCI id required"
	exit 1
fi

for ((i = 0; i < 0x8000; i = i + 4))
do
	reghex=`echo "obase=16; $i" | bc`

	setpci -s $1 78.l=$reghex

	val=`setpci -s $1 80.l`

	if [ $val != "00000000" ]; then
		printf "%04x: 0x$val\n" $i
	fi
done

