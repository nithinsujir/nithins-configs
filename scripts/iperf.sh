#!/bin/bash

THREADS=1
SERVER=1
TIME=10
REMOTE=1

while getopts "j:t:p:r:c" opt; do
	case "${opt}" in
		j)
			THREADS=${OPTARG}
			;;
		c)
			SERVER=0
			;;
		t)
			TIME=${OPTARG}
			;;
		r)
			REMOTE=${OPTARG}
			;;
		*)
			usage
			;;
	esac
done

index=1
for ((i = 0; i < $THREADS; i++)); do

	if [[ $SERVER -eq 1 ]]; then
		iperf -s -p $index$index$index$index -i 10 &
	else
		iperf -c $index.$index.$index.$REMOTE -p $index$index$index$index -t $TIME -i 10 &
	fi

	((index++))
done

wait
