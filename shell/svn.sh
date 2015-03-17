#!/bin/bash
#set -x

workspace=/home/nsujir/ws_svn
svnrepo=file:///home/nsujir/svnrepo

if [ $# -lt 2 ]
then
     echo "svn.sh <change list> <comment>";
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

fils=`p4 opened ... | grep $clist | grep -v "delete" | sed 's/#.*//;' | p4 -x - where |  sed 's/.*\/\/.* \//\//'`;

ws="$workspace/$clist";

if [ -a $ws ]
then
     echo "Workspace $clist exists. Updating";
else
     echo "Workspace $clist does not exist. Creating";
     mkdir $ws;

     svn import $ws $svnrepo/$clist -m "Init";
     svn co $svnrepo/$clist $ws;
fi


#Delete all links in workspace
rm $ws/*

for i in $fils ;
do
#filename=`echo $i | sed 's/.*\///'`;

    # Copy new version to workspace
    cp $i $ws;
done

svn add $ws/*
svn commit $ws -m "$comment";


#Delete all files in workspace and create links
rm $ws/*

for i in $fils ;
do
#filename=`echo $i | sed 's/.*\///'`;

    ln -s $i $ws;
done

