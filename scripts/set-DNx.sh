#!/bin/bash
model=$(product-model)

for d in `list_disks -R`; do
	disksig -w -p -m $model $d
	disksig -r $d
done

disksig -w -p -m $model `list_disks -i`
disksig -r `list_disks -i`

sed -i 's/T5080/DN2/' /var/lock/subsys/platform
sed -i 's/T5050/DN1/' /var/lock/subsys/platform

echo "disksig -m"
disksig-install -m
