#!/bin/bash

ticks=`cat /tmp/adjtimex.log | awk {'print $6;'} | tail -n 6`

i=0
for tick in $ticks ; do
	((i+=$tick))
done

((i/=60))

echo $i

