#!/bin/bash
SIZEM=$1
FILE1="/var/corefiles/rand1.bin"
PATTERN1="1"
FILE2="/var/corefiles/rand2.bin"
PATTERN2="2"
NVDIMMDEV=/dev/agigaram1
PATTERN_FILE=/tmp/pattern
PATTERN_FILE_SIZE=$((1024*1024))

# Create a 64k file with the given 1 byte pattern
create_pattern_file() {
	local i
	local pattern

	pattern=${2:1:1}

	rm -rf $PATTERN_FILE
	echo "Using pattern $pattern"
	for ((i=0; i<$PATTERN_FILE_SIZE; i++)); do
		echo $pattern >> $PATTERN_FILE
	done
}

# Write the 64 byte pattern file to 1G nvdimm
write_pattern() {
	local i
	for ((i=0; i<16384; i++)); do
		dd if=$PATTERN_FILE of=$NVDIMMDEV bs=64k seek=$i
	done
}

nvtag=$(head -c 1 $NVDIMMDEV)

if [[ $nvtag == $PATTERN1 ]]; then
	create_pattern_file $PATTERN2
else
	create_pattern_file $PATTERN1
fi

write_pattern

sync
#ipmitool power cycle

