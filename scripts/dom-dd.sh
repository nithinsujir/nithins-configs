#!/bin/bash

INDISK=$1
OUTDISK=$2
BS=${3:-4}

if [[ -z $INDISK || -z $OUTDISK ]]; then
	echo "$0 <indisk> <outdisk> [<block size in K> (default 4)]"
	exit 1
fi

while [ 1 ]; do
	dd if=$INDISK of=$OUTDISK bs=${BS}K oflag=direct
	sleep 1
done

