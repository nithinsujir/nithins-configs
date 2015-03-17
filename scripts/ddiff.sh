#!/bin/bash
#set -x

if [ $# -lt 1 ]
then
     echo "$0 <change list>";
     exit 1;
fi

clist=$1;

numfiles=`p4 describe $clist | wc -l`;
if [ $numfiles -eq 0 ]
then
     echo "Changelist does not exist";
     exit 1;
fi

numfiles=`p4 opened ... | grep $clist | wc -l`;
if [ $numfiles -eq 0 ]
then
     echo "Changelist not in this dir";
     exit 1;
fi

files=`p4 opened -c $1 | sed "s:#.*$::" | p4 -x - where | sed "s:.* ::"`

workspace=/home/nsujir/Depot/Departments/SystemsEngineering/users/nsujir/
cd $workspace/$clist

for file in $files; do
    dir=`dirname $file | sed "s:^/::"`
    name=`basename $file`

    differs=`diff $dir/$name $file | wc -l`

    if [ $differs  -ne 0 ]; then
        gvimdiff $dir/$name $file
    else
        echo "$file does not differ"
    fi
done

