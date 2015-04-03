#!/bin/bash

compver() {
	A=$1
	B=$2

	# Save to array
	local ifs=$IFS
	IFS=.
	a=($A)
	b=($B)
	IFS=$ifs

	# Compare
	for (( i = 0; i < 4; i++ )); do
		echo "${a[i]} ${b[i]}"

		if [[ ${a[i]} -eq ${b[i]} ]]; then
			continue
		fi

		if [[ ${a[i]} -gt ${b[i]} ]]; then
			return 1
		fi

		return 2

	done

	return 0
}






