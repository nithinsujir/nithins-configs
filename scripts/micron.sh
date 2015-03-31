#!/bin/bash

SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
LOG=/tmp/denali.log
OK="."
NOTOK="!!!"
DOWN="---"
echo "Denali Model and Upgrade status" > $LOG
echo "LEGEND - Ok: [$OK] NotOk: [$NOTOK] Down: [$DOWN]" >> $LOG
echo >> $LOG

log() {
	name=$1
	model=$2
	md=$3
	idom=$4
	ddom=$5


	printf "%8s    |%8s     |%8s     |%8s     |%8s    \n"  $name $model $md $idom $ddom >> $LOG
}

log "Name" "Model" "md" "idom" "ddom"

print_tgts() {
	for dn in m h; do
		for ((i=1; i<=15; i++)); do
			for cont in a b; do
				echo taf${dn}${i}${cont}
			done
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
	$SCP rootfscheck.sh root@$tgt:
	$SSH root@$tgt /root/rootfscheck.sh >> $LOG
	#log  $tgt $model $md $idom $ddom
done

