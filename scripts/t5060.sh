#!/bin/bash
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"
LOG=/tmp/t5060.log
OK="."
NOTOK="!!!"
DOWN="---"

print_tgts() {
	for dn in m; do
		for ((i=4; i<=25; i++)); do
			echo taf${dn}${i}
		done
	done
}


tgts=($(print_tgts))
if [[ ! -z $1 ]]; then
	tgts=($@)
fi

tgts=(tafm6)
for tgt in ${tgts[@]}; do
	echo "------------- $tgt ---------------" >> $LOG

	/bin/ping -c 1 -W 3 ${tgt}a
	if [[ $? -ne 0 ]]; then
		echo $tgt $DOWN
		continue
	fi

	/bin/ping -c 1 -W 3 ${tgt}b
	if [[ $? -ne 0 ]]; then
		echo $tgt $DOWN
		continue
	fi


	#$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x show"
	#$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x set \"Product Model\"=T5060"
	#$SSH root@$tgt "/usr/local/tintri/bin/fruinfo -x show"


	for cont in a b; do
		#$SSH root@${tgt}${cont} "/usr/local/tintri/bin/customer-model.sh"
		#continue

		tsa ${tgt}${cont}
		$SSH root@${tgt}${cont} "sed -i 's/5050/5060/' /var/lock/subsys/platform"
		rdisks=$($SSH root@${tgt}${cont} "/usr/local/tintri/bin/list_disks -R")
		for rd in $rdisks; do
			$SSH root@${tgt}${cont} "/usr/local/tintri/bin/disksig -w -p -m T5060 $rd"
		done
		bdom=$($SSH root@${tgt}${cont} "/usr/local/tintri/bin/list_disks -i")
		$SSH root@${tgt}${cont} "/usr/local/tintri/bin/disksig -w -p -m T5060 $bdom"
	done
done

