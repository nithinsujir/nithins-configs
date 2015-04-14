#!/bin/bash
model=$(product-model)

for d in `list_disks -R`; do
	disksig -w -p -m $model $d
	disksig -r $d
done

disksig -w -p -m $model `list_disks -i`
disksig -r `list_disks -i`

echo "disksig -m"
disksig-install -m
