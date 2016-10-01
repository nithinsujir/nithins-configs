#!/bin/bash
GIT=/usr/local/bin/git
BRANCHES=( default-4.4 )
GERRIT_CLONE=/data/gerrit/gerrit-kernel

cd $GERRIT_CLONE
for branch in ${BRANCHES[@]}; do
	echo "Sync $branch"
	$GIT checkout $branch
	$GIT pull gitlab $branch
	$GIT push
done

