#!/bin/bash

set -x
set -e

rels=`ls -1 $1 | grep ^3.1..[a-z]\$`

echo $rels

rm -rf git-tg3-rels
mkdir git-tg3-rels
cd git-tg3-rels
git init
touch .x
git add .x
git commit -am "dummy init"

for d in $rels
do
	tar zxvf $1/$d/tg3-$d.tar.gz
	cp tg3-$d/* .
	if [ -f $1/$d/RELEASE.TXT ]
	then
		cp $1/$d/RELEASE.TXT .
	fi

	rm -rf tg3-$d
	dos2unix *
	git add *
	git commit -am $d
done


