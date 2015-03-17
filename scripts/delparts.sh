#!/bin/bash

for disk in `./list_disks -h`
do
	for part in `seq 7`
	do
		parted -s $disk rm $part
	done
done

