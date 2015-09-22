#!/bin/bash
if grep -q pmc_nvram /proc/modules; then
	echo "Warning reloading pmc_nvram. System will crash in a little bit"
	rmmod pmc_nvram
fi

if grep -q pmc /proc/modules; then
	echo "Warning reloading pmc. System will crash in a little bit"
	rmmod pmc
fi

if grep -q nvx /proc/modules; then
	echo "Warning reloading nvx System will crash in a little bit"
	rmmod nvx
fi

insmod /root/nvx.ko
if [[ $? -ne 0 ]]; then
	echo "Error loading nvx"
	exit 1
fi

insmod /root/pmc.ko
if [[ $? -ne 0 ]]; then
	echo "Error loading pmc"
	exit 1
fi

modprobe pmc_nvram
if [[ $? -ne 0 ]]; then
	echo "Error loading pmc_nvram"
	exit 1
fi

md5sum /root/nvx.ko
md5sum /root/pmc.ko

pmctool.py -b

