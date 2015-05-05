#!/bin/bash

SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"

print_tgts() {
	for dn in m h; do
		for ((i=1; i<=15; i++)); do
			echo taf${dn}${i}
		done
	done
}


tgts=($(print_tgts))
if [[ ! -z $1 ]]; then
	tgts=($@)
fi

echo "Corefile Partition Upgrade Status"
for tgt in ${tgts[@]}; do
	echo -n "$tgt: "
	/bin/ping -c 1 -W 3 $tgt 2>&1 > /dev/null
	if [[ $? -ne 0 ]]; then
		echo "            *** Not reachable!"
		continue
	fi

	tsa $tgt 2>&1 > /dev/null
	corepart=$($SSH root@$tgt "/bin/grep md0p6 /proc/partitions" | /usr/bin/awk {'print $3;'})

	if [[ $? -eq 0 ]]; then
		if [[ $corepart -gt 85000000 ]]; then
			echo "      Yes"
		else
			echo "                                       *** No!!"
		fi
	else
		echo "Unable to determine core partition size"
	fi
done

