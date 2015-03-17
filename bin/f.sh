#!/usr/bin/env bash
# Create a list of files in .f for fuzzyfinder to open

dirs=(
	block
	drivers/hwmon
	drivers/net/bnx2*
	drivers/net/bnx2x
	drivers/net/cnic*
	drivers/scsi/bnx2fc
	drivers/scsi/fcoe
	drivers/scsi/libfc
	drivers/scsi/sc*
	include/asm-generic
	include/linux
	include/scsi
	kernel
	mm 
	net/8021q
	net/core
	net/ethernet
	net/ipv*
	net/llc
	net/netlink
	net/packet
	net/sock*
	)

rm -rf .fufcache
mkdir -p .fufcache
cd .fufcache

#for dirname in ${dirs[@]}; do
for fil in `cat ../cscope.files`; do
	echo $fil
	ln -sf ../$fil .
done


