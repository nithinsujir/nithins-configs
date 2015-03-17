#!/bin/bash

set -e

bdom=$(/usr/local/tintri/bin/list_disks -i)
ddom=$(/usr/local/tintri/bin/list_disks -d)

dd if=/dev/zero of=$bdom count=99
sync
sfdisk -R $bdom
/usr/local/tintri/bin/partition_haboot $bdom

# Repeatedly do inst_grub and inst_bootfiles
for ((i = 0; i < 1000; i++)); do
	echo "Iteration: $i"

	/usr/local/tintri/bin/inst_grub $bdom
	/usr/local/tintri/bin/inst_bootfiles $ddom $bdom
done


