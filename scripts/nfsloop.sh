#!/bin/bash
set -e

for ((i = 1; i <= 10000; i++))
do
	echo "Iteration: $i"
	python nfstest.py -s $1 -c $2
done

