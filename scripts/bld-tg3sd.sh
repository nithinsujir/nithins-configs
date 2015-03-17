#!/usr/bin/env bash

# Clear old files
NSEG_DIR=/media/nseg/rels/tg3/tg3sd
set -x
set -e

rm -rf tg3sd
find /usr/src/packages -name "*.rpm" | xargs rm -f
find /usr/src/packages -name "*.tar.gz" | xargs rm -f

git clone nsujir@nl2:gtsd
cd gtsd
./configure --sbindir=/usr/sbin --sysconfdir=/etc
make dist
mv *.gz /usr/src/packages/SOURCES
rpmbuild -ba tg3sd.spec

version=`grep Version tg3sd.spec | awk ' {print $2}'`
mkdir -p $NSEG_DIR/$version

find /usr/src/packages -name "*.rpm" | xargs -I xxx mv xxx $NSEG_DIR/$version
find /usr/src/packages -name "*.tar.gz" | xargs -I xxx mv xxx $NSEG_DIR/$version
cp ../README $NSEG_DIR/$version
