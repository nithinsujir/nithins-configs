#!/bin/bash
DEV=$1
set -x
set -e
while [ 1 ] ; do
	sudo ./tools/nvram/nvx -I -n 888M -v -V  -x -k -f $DEV
	sleep 1
done
