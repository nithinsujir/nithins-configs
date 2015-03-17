#!/bin/bash
DISK=$1
DELAY=${2:-10}

while [ 1 ]; do
	date
	iostat -m $DISK
	smartctl -x $DISK | grep -i endu
	smartctl -a $DISK | grep -i wear
	sleep $DELAY
done

