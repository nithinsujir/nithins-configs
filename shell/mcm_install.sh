#!/bin/bash
RLS=$1
CWD=`pwd`

cd $HOME
ln -sf $CWD/../tar_ne/$RLS.x86.tar.gz .

$CWD/../scripts/mcm_install +i -base_dir base -rls $RLS -ins

chmod -R 755 base/ins/$RLS

rm $HOME/base/ins/current
ln -sf $HOME/base/ins/$RLS $HOME/base/ins/current
