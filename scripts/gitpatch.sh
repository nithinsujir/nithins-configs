#!/bin/bash
set -x
set -e

patchdir=$1
numpatches=$2
branch="pobo"

CPUS=`grep processor /proc/cpuinfo | wc -l`

git status | grep clean
git checkout master

git checkout -b $branch

make -j $CPUS > bld.log

for ((i = 1; i <= $numpatches; i++))
do
	var=$(printf '%04d-' $i)
	git am $1/$var*
	./scripts/checkpatch.pl $1/$var*

	make -j $CPUS
done

git checkout master
git branch -D $branch
