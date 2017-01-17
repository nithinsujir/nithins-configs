#!/bin/bash
GIT=/usr/local/bin/git
REPOS=( gerrit-kernel gerrit-utils )
declare -A BRANCHES=( \
	['gerrit-kernel']='default-4.4 '\
	['gerrit-utils']='master')
CLONE_DIR=/data/gerrit/

for repo in ${REPOS[@]}; do
	cd $CLONE_DIR/$repo

	branches=("${BRANCHES[$repo]}")
	for branch in ${branches[@]}; do
		echo "Sync $repo:$branch"
		$GIT checkout $branch
		$GIT pull gitlab $branch
		$GIT push
	done
done

