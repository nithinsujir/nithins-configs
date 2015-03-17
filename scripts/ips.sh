#!/bin/bash

IP_END=${1:-1}
shift

ETHS=()

for i in 0 1 2 3; do
	ETHS+=($(ls -l /sys/class/net/*/device | grep 83:00.$i | sed 's/.*.eth/eth/' | sed 's:/.*$::'))
done

ip=1

for eth in ${ETHS[@]}; do
	echo "ifconfig $eth $ip.$ip.$ip.$IP_END up"
	ifconfig $eth $ip.$ip.$ip.$IP_END up
	((ip++))
done

