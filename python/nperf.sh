#!/bin/bash

total=0
for i in {1..10}
do
	`./nperf.py -i $1 | grep 16384 | awk '{print $5;}'
	sleep 1
done

