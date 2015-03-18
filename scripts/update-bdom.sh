#!/bin/bash
# This script will update the internal boot dom on the given machine by
# extracting the required boot files from the given rpm
# The boot directory from the rpm is scp'd to the target and used to copy over
# the internal dom

TARGET=
RPM=
SCP="/usr/bin/scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
SSH="/usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"

run() {
	cmd="$@"

	$cmd
	status=$?

	if [[ $status -ne 0 ]]; then
		echo "$cmd failed with status $status"
		exit 1
	fi
}

while getopts "t:r:" opt; do
	case "${opt}" in
		t)
			TARGET=${OPTARG}
			;;
		r)
			RPM=${OPTARG}
			;;
		*)
			usage
			;;
	esac
done

if [[ -z $TARGET || -z $RPM ]]; then
	usage
fi

# Extract the boot folder from the rpm
tempdir=$(run /bin/mktemp -d)
echo $tempdir

cd $tempdir
/usr/bin/rpm2cpio $RPM | /bin/cpio -icvd --no-absolute-filenames ./var/relarchive/txos*/base_os*
if [[ $? -ne 0 ]]; then
	echo "Error extracting base_os rpm"
	exit 2
fi

/usr/bin/rpm2cpio ./var/relarchive/txos*/base_os*.rpm | /bin/cpio -icvd --no-absolute-filenames ./boot/*
if [[ $? -ne 0 ]]; then
	echo "Error extracting boot folder"
	exit 3
fi


/bin/cat > mdadm.conf <<-EOF
ARRAY /dev/md0 metadata=1.2 name=(none):0 UUID=aaaaaaaa:bbbbbbbb:cccccccc:dddddddd
EOF

$SCP mdadm.conf root@$TARGET:/tmp
if [[ $? -ne 0 ]]; then
	echo "Error scp'ing mdadm.conf"
	exit 4
fi

$SCP -r ./boot root@$TARGET:/tmp
if [[ $? -ne 0 ]]; then
	echo "Error scp'ing boot folder"
	exit 5
fi


bdom=$($SSH root@$TARGET "/usr/local/tintri/bin/list_disks -i")
if [[ $? -ne 0 ]]; then
	echo "Error determining boot dom"
	exit 6
fi


$SSH root@$TARGET "/usr/local/tintri/bin/inst_bootfiles /tmp $bdom"
if [[ $? -ne 0 ]]; then
	echo "Error installing bootfiles on target"
	exit 7
fi

cd ..
/bin/rm -rf $tempdir

