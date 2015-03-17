#!/bin/bash

ifaces=($(ls -l /sys/class/net/*/device | grep 83 | sed 's/.*.eth/eth/' | sed 's:/.*$::'))

for iface in ${ifaces[@]}; do
	echo "Interface: $iface"
	echo "ethtool"
	ethtool $iface

	echo "ethtool -k"
	ethtool -k $iface

	echo "ethtool -c"
	ethtool -c $iface

	echo "ethtool -g"
	ethtool -g $iface

	echo "ethtool -i"
	ethtool -i $iface
done

lspci -vvv -t
lspci -vvv
lspci -vvv -s 83:00

while read line; do
	tmp=${line%%:*}
	intr=${tmp//[[:space:]]}

	if [[ $line =~ i40e ]]; then
		aff=$(cat /proc/irq/$intr/smp_affinity)
		label=$(echo $line | sed 's/.* //')

		echo "$label: $aff"
	fi
done < /proc/interrupts
