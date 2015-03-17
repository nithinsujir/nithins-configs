#!/bin/bash
set -x
set -e

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

files=`p4 opened -c $1 | sed "s:#.*$::" | p4 -x - where | sed "s:.* ::"`

workspace=/home/nsujir/Depot/Departments/SystemsEngineering/users/nsujir/

# Delete existing directory if any
mkdir -p $workspace/$clist
cd $workspace/$clist
export P4CLIENT=nsujir-rb-misc

for file in $files; do
    dir=`dirname $file | sed "s:^/::"`
    mkdir -p $dir
    name=`basename $file`

    p4 edit $dir/$name
    cp $file $workspace/$clist/$dir

    p4 add $dir/$name
done

p4 revert -a ...
p4 change -o | sed -e "s/.enter description here./$comment/" | p4 submit -i
