#!/bin/bash
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
LOG=/tmp/denali.log
OK="."
NOTOK="!!!"
DOWN="---"

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

for tgt in ${tgts[@]}; do
	echo "------------- $tgt ---------------" >> $LOG

	/bin/ping -c 1 -W 3 $tgt
	if [[ $? -ne 0 ]]; then
		log $tgt $DOWN
		continue
	fi

	tsa $tgt
	$SCP /tmp/platform_common root@$tgt:/usr/local/tintri/bin/
	$SCP /tmp/xy_fruinfo.sh root@$tgt:/usr/local/tintri/bin/

	if [[ $tgt =~ tafm[0-9]+ ]]; then
		model="T5050"
	else
		model="T5080"
	fi

	$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x show"
	$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x set \"Product Model\"=$model"
	$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x show"
done

