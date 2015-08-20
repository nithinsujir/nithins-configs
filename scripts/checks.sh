#!/bin/bash
set -e

d0=$(list_disks -c 0)
echo "Controller 0 disks: $d0"

d1=$(list_disks -c 1)
echo "Controller 0 disks: $d1"

h=$(list_disks -h)

for d in $h; do
	echo "-------------- $d ---------------"
	disksig -r $d

	fsck ${d}1
done

