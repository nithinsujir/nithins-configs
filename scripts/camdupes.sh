#!/bin/bash
# This script removes backed up duplicates from the camera folder. The sony
# import program has a folder pattern of m-d-yyyy. The camera has the pattern
# ????ddmm.
# mount the borg backup to check at /tmp/bmount. Connect camera so that f:\...
# is present. Restart ubuntu to automount these shared folders.
re="([[:digit:]]+)-([[:digit:]]+)-[[:digit:]]+"
CAMDIR_BASE=/media/sf_DCIM
BDIR_BASE=/tmp/bmount/cifs/lhdd2/data-source/pictures
pdirs=($(ls -1 $BDIR_BASE | grep -e "\-.\-" -e "\-..\-"))

# touch the files in the camdir. fdupes sorts by oldest to newest. Since we
# want the camera dir duplicates to be deleted, it should be 2nd in the list.
find $CAMDIR_BASE | xargs touch

for pdir in ${pdirs[@]}; do
	if [[ $pdir =~ $re ]]; then
		cdir=$(printf "%02d%02d" ${BASH_REMATCH[1]} ${BASH_REMATCH[2]})
		cdir=$(ls -1 $CAMDIR_BASE/ | grep $cdir | head -n 1)

		if [[ ! -z $cdir ]]; then
			echo "fdupes $BDIR_BASE/$pdir $CAMDIR_BASE/$cdir"
			fdupes $BDIR_BASE/$pdir $CAMDIR_BASE/$cdir -N -d
		fi
	fi
done
