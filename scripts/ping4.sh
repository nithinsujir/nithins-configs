#!/bin/bash

REMOTE=${1:-1}

for i in 1 2 3 4; do
	ping -c 2 $i.$i.$i.$REMOTE
done

