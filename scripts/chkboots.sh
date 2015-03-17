#!/bin/bash
set -x

mkdir -p /d1
mkdir -p /d2
mkdir -p /d3

disks=$(list_disks -R)
mnt=1
ctrlid=$(get_ctrlid)
part=1

for disk in $disks; do
	mount ${disk}${part} /d$mnt
	((mnt+=1))

	if [[ $ctrlid -eq 1 ]]; then
		part=6
	fi
done

diff /d1/initrd-p1 /d2/initrd-p1
diff /d2/initrd-p1 /d3/initrd-p1

diff /d1/initrd-p2 /d2/initrd-p2
diff /d2/initrd-p2 /d3/initrd-p2

diff /d1/vmlinuz-p1 /d2/vmlinuz-p1
diff /d2/vmlinuz-p1 /d3/vmlinuz-p1

diff /d1/vmlinuz-p2 /d2/vmlinuz-p2
diff /d2/vmlinuz-p2 /d3/vmlinuz-p2

umount /d1
umount /d2
umount /d3

