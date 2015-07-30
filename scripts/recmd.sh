#!/bin/bash
set -e
set -x
export PATH=$PATH:/usr/local/tintri/bin
ctrlid=$(get_ctrlid)

if [[ -b /dev/md0 ]]; then
	mdadm --stop /dev/md0
fi

set +e
HddMdPart=5
for d in $(list_disks -c $ctrlid); do
	mdadm --zero-superblock ${d}${HddMdPart}
done
set -e

create_md
partition_md

for part in 1 2 3 5 6; do
	mkfs -t ext3 /dev/md0p$part
	/sbin/tune2fs -c 10 /dev/md0p$part
done

mkswap /dev/md0p7

# Update disksigs
tokens=($(/sbin/mdadm -D /dev/md0 | grep UUID))
mduuid=${tokens[2]}
for d in $(list_disks -c $ctrlid); do
	disksig -w -p -u $mduuid -c $ctrlid $d
done
disksig -w -p -u $mduuid -c $ctrlid /dev/sda

MdDev=md0
partno=p1
MdLogPart=3
MdSqlPart=5
loc_bindir=/usr/local/tintri/bin/

mount -t ext3 /dev/${MdDev}${partno} /sysroot 
mkdir -p /sysroot/var/log
mkdir -p /sysroot/var/pgsql
mount -t ext3 /dev/${MdDev}p${MdLogPart} /sysroot/var/log
mkdir -p /sysroot/var/log/tintri
mount -t ext3 /dev/${MdDev}p${MdSqlPart} /sysroot/var/pgsql
mkdir -p /sysroot/var/pgsql/shared

${loc_bindir}/inst_sw $relflag /sysroot /mnt/releases
${loc_bindir}/inst_boot /sysroot 
${loc_bindir}/postinst_config -${partno} /sysroot 

cp /sysroot/usr/tintri/etc/procmon-cfg.default.js /sysroot/etc/sysconfig/tintri/procmon-cfg.js
cp /sysroot/usr/tintri/etc/realstore-cfg.default.js /sysroot/var/pgsql/shared/realstore-cfg.js


/bin/cp /tmp/InstallLogFile.txt /sysroot/var/log/tintri/platform
/bin/sync
umount /sysroot/var/pgsql
umount /sysroot/var/log
umount /sysroot 

partno=p2
mount -t ext3 /dev/${MdDev}${partno} /sysroot
mkdir -p /sysroot/var/log
mkdir -p /sysroot/var/pgsql
mount -t ext3 /dev/${MdDev}p${MdLogPart} /sysroot/var/log
mount -t ext3 /dev/${MdDev}p${MdSqlPart} /sysroot/var/pgsql

${loc_bindir}/inst_sw  $relflag /sysroot /mnt/releases
${loc_bindir}/postinst_config -${partno} /sysroot 

cp /sysroot/usr/tintri/etc/procmon-cfg.default.js /sysroot/etc/sysconfig/tintri/procmon-cfg.js
cp /sysroot/usr/tintri/etc/realstore-cfg.default.js /sysroot/var/pgsql/shared/realstore-cfg.js

/bin/touch /sysroot/var/log/tintri/platform/install.success

sync
umount /sysroot/var/pgsql
umount /sysroot/var/log
umount /sysroot 

sync

echo "TODO: check and wait for md resync"

