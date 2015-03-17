#!/bin/bash
from=$(product-model)

if [[ $from == "DN1" ]]; then
	to=T950
elif [[ $from == "DN2" ]]; then
	to=T980
else
	echo "Unsupported platform $from"
	exit 1
fi

tofam=T900
fromfam=Denali

parted /dev/sda set 1 boot on
dd if=/dev/zero of=/dev/sdb count=99
sync


sed -i 's/'$from'/'$to'/' /opt/tintri/platform-model.sh
sed -i 's/'$from'/'$to'/' /var/lock/subsys/platform
sed -i 's/"'$from'"/"'$to'"/' /usr/local/tintri/bin/platform_common
sed -i 's/"'$fromfam'"/"'$tofam'"/' /usr/local/tintri/bin/platform_common

for d in `list_disks -R`; do
	disksig -w -p -m $to $d
done

echo "product model"
product-model

echo "disksig -m"
disksig-install -m

cat /var/lock/subsys/platform
cat /opt/tintri/platform-model.sh
grep -e DN -e T9 /usr/local/tintri/bin/platform_common
