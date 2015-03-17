#!/bin/bash
MTU=${1:-9000}
for ((i=0; i < 4; i++)); do
	ifconfig bonddata$i mtu $MTU
	slave=$(cat /proc/net/bonding/bonddata0 | grep "Active Slave" | sed 's/.*://')
	ifconfig $slave mtu $MTU
done

ip addr show | grep bondd


