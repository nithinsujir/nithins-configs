#!/bin/bash

for r in `ls *.rpm`; do
	pam=$( rpm -qpR $r | grep ^pam )

	if [ $? -eq 0 ]; then
		echo
		echo "--------- $r ---------"
		echo $pam
	fi
done
