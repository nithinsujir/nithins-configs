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

echo "          Model Upgrade Status"
echo "---------------------------------------------------"
for tgt in ${tgts[@]}; do
	/bin/ping -c 1 -W 3 $tgt 2>&1 > /dev/null
	if [[ $? -ne 0 ]]; then
		result="   [Unreachable]"
		sysvers="[Unknown]"
	else
		tsa $tgt 2>&1 > /dev/null
		sysvers=
		dsig_model=$($SSH root@$tgt "/usr/local/tintri/bin/disksig-install -m")

		if [[ $? -eq 0 ]]; then
			if [[ $dsig_model =~ DN ]]; then
				result="       No!"
				sysvers=$($SSH root@$tgt "/usr/local/tintri/bin/sysvers")
			else
				result="                            Yes"
			fi
		else
			result="disksig-install -m failed"
		fi
	fi

	printf "%08s %30s %s\n" $tgt "$sysvers" "$result"
done

