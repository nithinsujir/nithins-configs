#!/bin/bash
#set -x

curdir=$PWD
curclient=$P4CLIENT

workspace=/home/nsujir/part2/depot/users/nsujir
if [ $# -lt 2 ]
then
     echo "$0 <change list> <comment>";
     exit 1;
fi

clist=$1;
comment=$2;


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

fils=`p4 opened ... | grep $clist | grep -v "delete" | sed 's/#.*//;' | p4 -x - where |  sed 's/.*\/\/.* \//\//' | sed 's/.*\/ixos\///' | sed 's/[a-zA-Z0-9\.]*\///'`;

cd $workspace;
ln -sf $curdir $workspace/$clist
export P4CLIENT=nsujir-depot

for i in $fils ;
do
p4 add $clist/$i
p4 edit $clist/$i
done

depot_opened=`p4 opened ... | sed 's/.*nsujir\///' | sed 's/#.*//'`
p4 revert -a ...
p4 change -o | sed -e "s/.enter description here./$comment/" | p4 submit -r -i

#Revert makes file read only. Fix
for i in $depot_opened ;
do
p4 edit $i;
done

cd $curdir
export P4CLIENT=$curclient
