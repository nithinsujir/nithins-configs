#!/bin/bash

SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"

print_tgts() {
	for dn in m h; do
		for ((i=1; i<=18; i++)); do
			echo taf${dn}${i}
		done
	done
}


tgts=($(print_tgts))
if [[ ! -z $1 ]]; then
	tgts=($@)
fi

echo "                    Corefile Partition Upgrade Status"
echo "---------------------------------------------------------------------------"
for tgt in ${tgts[@]}; do
	/bin/ping -c 1 -W 3 $tgt 2>&1 > /dev/null
	if [[ $? -ne 0 ]]; then
		result="   [Unreachable]"
		sysvers="[Unknown]"
	else
		tsa $tgt 2>&1 > /dev/null
		corepart=$($SSH root@$tgt "/bin/grep md0p6 /proc/partitions" | /usr/bin/awk {'print $3;'})
		sysvers=

		if [[ $? -eq 0 ]]; then
			if [[ $tgt =~ tafh ]]; then
				coremin=150000000
			else
				coremin=90000000
			fi

			if [[ $corepart -gt $coremin ]]; then
				result="                            Yes"
			else
				result="       No!"
				sysvers=$($SSH root@$tgt "/usr/local/tintri/bin/sysvers")
			fi
		else
			result="Unable to determine core partition size"
		fi
	fi

	printf "%08s %30s %s\n" $tgt "$sysvers" "$result"
done

