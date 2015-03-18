#!/bin/bash

mkdir -p /bdom
mkdir -p /ddom

umount /bdom
umount /ddom


bdom=$(/usr/local/tintri/bin/list_disks -i)
ddom=$(/usr/local/tintri/bin/list_disks -d)

umount ${bdom}1
umount ${ddom}1

set -e
# Repeatedly do inst_grub and inst_bootfiles
for ((i = 0; i < 99999; i++)); do
	echo "Iteration: $i"
	# Partition
	dd if=/dev/zero of=$bdom count=99
	sync
	sleep 2
	sfdisk -R $bdom
	sleep 2
	/usr/local/tintri/bin/partition_haboot $bdom

	# Install
	/usr/local/tintri/bin/inst_grub $bdom
	/usr/local/tintri/bin/inst_bootfiles $ddom $bdom

	# Verify
	mount ${bdom}1 /bdom
	mount ${ddom}1 /ddom

	for fil in initrd System.map vmlinuz; do
		for ((j = 1; j <= 2; j++)); do
			diff /bdom/${fil}-p$j /ddom/${fil}-p$j
		done
	done

	umount /ddom
	umount /bdom

	dmesg -c | grep sdb
	sleep 1
done

