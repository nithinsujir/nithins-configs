#!/bin/bash
partition_hdd /dev/sdc
partition_hdd /dev/sdd
partition_hdd /dev/sde

mdadm --create /dev/md1 --level=raid10 -c 256 -p n3 --bitmap=internal --run --metadata=1.2 --raid-devices=3 /dev/sdc1 /dev/sdd1 /dev/sde1
