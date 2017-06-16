#!/bin/bash
set -x

HOST=tboltsr37
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error -l root"

while [[ 1 ]]; do
	i=$((i++))

	echo "Iteration: $i"

	$SSH ${HOST}a "ifconfig eth6 down"
	$SSH ${HOST}a "ifconfig eth7 down"

	$SSH ${HOST}b "ifdown bondinternal0"
	sleep 1
	$SSH ${HOST}b "ifup bondinternal0"

	$SSH ${HOST}b "ip addr show | grep bondinternal"

	$SSH ${HOST}a "ifconfig eth6 up"
	$SSH ${HOST}a "ifconfig eth7 up"

	sleep 10

	$SSH ${HOST}b "ip addr show | grep bondinternal | grep DOWN"
	if [[ $? -eq 0 ]]; then
		echo "Link not up"
		break
	fi
done

