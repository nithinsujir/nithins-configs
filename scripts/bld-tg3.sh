#!/usr/bin/env bash

# Clear old files
VER=$1
NSEG_DIR=/media/nseg/rels/tg3
#NSEG_DIR=/tmp/tg3

set -x
set -e

rm -rf tg3-$VER
git clone nsujir@nl2:gtn tg3-$VER
tar jcvf tg3-$VER.tar.bz2 tg3-$VER --exclude .git
tar zcvf tg3-$VER.tar.gz tg3-$VER --exclude .git
mv tg3-$VER.tar.bz2 $HOME/rpmbuild/SOURCES

sed "s/define brcmvers .*$/define brcmvers $VER/" tg3.spec  > tg3.tmp && mv tg3.tmp tg3.spec
rpmbuild -ba tg3.spec

sudo mkdir -p $NSEG_DIR/$VER

unix2dos tg3-$VER/README.TXT
unix2dos tg3-$VER/ChangeLog
unix2dos tg3-$VER/RELEASE.TXT

sudo cp tg3-$VER/README.TXT $NSEG_DIR/$VER
sudo cp tg3-$VER/ChangeLog $NSEG_DIR/$VER
sudo cp tg3-$VER/RELEASE.TXT $NSEG_DIR/$VER

sudo mv tg3-$VER.tar.gz $NSEG_DIR/$VER
sudo mv $HOME/rpmbuild/SRPMS/tg3-$VER-1.src.rpm $NSEG_DIR/$VER

rm -rf tg3-$VER
