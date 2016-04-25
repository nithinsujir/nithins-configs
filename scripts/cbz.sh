#!/bin/bash

for d in $(ls); do
	if [[ -d $d ]]; then
		zip $d.cbz $d/*
	fi
done

