#!/bin/bash
set -x
sync
DUMP_LEVEL=/sys/module/diskdump/parameters/dump_level

echo $1 > $DUMP_LEVEL
cat $DUMP_LEVEL

sleep 5

echo c > /proc/sysrq-trigger

