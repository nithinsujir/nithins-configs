#!/bin/bash

set -e

target=$1

if [[ $target == "" ]] ; then
	echo "Need remote target"
	exit 0
fi

for (( i = 0; $i < 100; i++ )); do
	echo "Iteration: $i"
	ssh root@$target "touch /var/corefiles/dum"
	ssh root@$target "ls -l /var/corefiles/*"
	echo "sleep 30"
	sleep 30
	ssh root@$target "ls -l /var/corefiles/*"
	ssh root@$target "rm -rf /var/corefiles/* &"
	echo "sleep 10"
	sleep 10
	ssh root@$target "ipmitool mc watchdog off"
	ssh root@$target "ipmitool bmc watchdog off"
	ssh root@$target sync
	ssh root@$target "/bin/sysrq &"

	echo "sleep 600"
	sleep 600
done


