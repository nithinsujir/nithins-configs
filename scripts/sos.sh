#!/bin/bash

iter=0
rm /tmp/sosreport*

logdir=sos-$(date +%d%b%y-%H%M)
mkdir -p $logdir/0
sosreport --batch -o networking,system,hardware,general,process,startup
mv /tmp/sosreport* $logdir/$iter
ifconfig | grep Ethernet | awk '{print $1;}' | xargs sudo mii-tool -vvv > $logdir/$iter/mii-tool.txt
cat /proc/interrupts > $logdir/$iter/interrupts.txt

while [ 1 ]
do
	iter=$(( $iter + 1 ))
	echo "Iteration $iter"
	mkdir -p $logdir/$iter
	sosreport --batch -o networking
	mv /tmp/sosreport* $logdir/$iter
	ifconfig | grep Ethernet | awk '{print $1;}' | xargs sudo mii-tool -vvv > $logdir/$iter/mii-tool.txt
	cat /proc/interrupts > $logdir/$iter/interrupts.txt

	sleep 1
done
