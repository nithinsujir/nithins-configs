#!/bin/bash
fils=$2

for fil in $@ ; do
    if [ $fil == $1 ] ; then 
        continue
    fi

    echo "Link: $fil -> $1"
    ln -sf $fil $1
done
