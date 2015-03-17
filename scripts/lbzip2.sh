#!/bin/bash

set -e
set -x

for ((i=0; i<1000; i++)); do
	echo "Iteration: $i"

	openssl rand -out random.bin -base64 $(( 2**31 * 2**3 ))

	md5=$(md5sum random.bin)

	lbzip2 -1 random.bin
	lbzip2 -d random.bin.bz2

	md5_2=$(md5sum random.bin)

	if [[ "$md5" != "$md5_2" ]]; then
		echo "Does not match $md5 $md5_2"
		exit
	else
		echo "Match: $md5"
	fi
done

