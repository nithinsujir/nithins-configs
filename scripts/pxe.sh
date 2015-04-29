#!/bin/bash
# This script does a pxe re-install on an already installed vmstore
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=error -l root"
SCP="scp -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
PXE_PATH="/tftpboot/pxelinux.cfg/"
HEADSTART=$((20 * 60))

# The name for the pxe install file has to be of the form 01-aa-bb-cc-dd-ee-ff.
# i.e. 01 followed by lower case mac with : replaced with -
pxefy_mac() {
	local mac=$1
	local name

	# Convert to lower case
	name=${mac,,}

	# Convert all : to -
	name=${name//:/-}

	echo "01-$name"
}

countdown() {
	local time=$1

	for (( i = 1; i < $time; i++ )); do
		sleep 1

		if (( i % 100 == 0 )); then
			echo "Waited $i seconds"
		fi
	done

	return 1
}

# Wait upto timeout for cmd to succeed
countdown_cmd() {
	local timeout=$1
	shift
	local cmd="$@"
	local i

	for (( i = 1; i < $timeout; i++ )); do
		$cmd 2>&1 > /dev/null
		if [[ $? -eq 0 ]]; then
			return 0
		fi

		sleep 1

		if (( i % 100 == 0 )); then
			echo "Waited $i seconds"
		fi
	done

	return 1
}

create_pxe_file() {
	local filename=$1
	local tgt=$2
	local ipaddr=$(/usr/bin/dig +short ${target}.tintri.com)
	local rel=$($SSH pxesrv1 "/usr/bin/readlink /var/ftp/txos_releases/latest")
	rel=${rel/-release-ndu/}
	rel=${rel/-release-du/}

	/bin/cat > /tmp/$filename <<-EOF
# Auto pxe install for $tgt
default txos

LABEL txos
        MENU LABEL latest trunk (tty console)
        KERNEL images/txos/latest/vmlinuz
        APPEND initrd=images/txos/latest/initrd verbose NukeInstall rootpart=1 stable=1 md_uuid=placeholder dev_uuid=placeholder devinstall nowdog ipaddr=${ipaddr} netmask=255.255.0.0 gateway=10.40.0.1 devpassword=tintri99 installvers=$rel
	
	EOF
}

stop_services() {
	# Stop services on secondary so as to not interfere
	$SSH $target "/usr/bin/ssh tt-peer-controller. \"/usr/tintri/bin/ProcMonCmd -s disabled realstore\""
	$SSH $target "/usr/bin/ssh tt-peer-controller. \"/sbin/service hamon stop\""
	$SSH $target "/usr/bin/ssh tt-peer-controller. \"/sbin/service platmon stop\""
	$SSH $target "/usr/bin/ssh tt-peer-controller. \"/sbin/service txos stop\""
}

wipe_and_reboot() {
	local tgt=$1

	echo "Clearing partitions on $tgt"
	$SSH $tgt "/bin/dd if=/dev/zero of=/dev/sda count=1024"
	$SSH $tgt "/bin/dd if=/dev/zero of=/dev/sdb count=1024"
	$SSH $tgt "/bin/sync"

	echo "Rebooting $tgt"
	$SSH $tgt "/usr/bin/ipmitool chassis power cycle"
}

wait_until_up() {
	local i
	local TGT_WAIT=6600
	local PEER_WAIT=1800

	echo "Waiting upto $TGT_WAIT sec for $target to be up"
	# Wait until target is up
	countdown_cmd $TGT_WAIT /bin/ping -c 1 -W 3 $target
	if [[ $? -ne 0 ]]; then
		echo "Timeout waiting for $target to be up"
		return 1
	fi
	echo "$target is up"

	# Wait until peer is up
	echo "Waiting upto $PEER_WAIT for peer to be up"
	tsa $target
	countdown_cmd $PEER_WAIT $SSH $target "/bin/ping -c 1 -W 3 tt-peer-controller."
	if [[ $? -ne 0 ]]; then
		echo "Timeout waiting for peer to be up"
		return 1
	fi
	echo "Peer is up"

	return 0
}


if [[ -z $1 ]]; then
	echo "Usage: $0 <system>"
	exit
fi

target=$1
echo "PXE Installing $target"

A=${target}a
B=${target}b


/bin/ping -c 1 -W 3 $A
if [[ $? -ne 0 ]]; then
	echo "Unable to ping $A"
	exit 1
fi
echo "$A is up"

/bin/ping -c 1 -W 3 $B
if [[ $? -ne 0 ]]; then
	echo "Unable to ping $B"
	exit 1
fi
echo "$B is up"

tsa $A
tsa $B

# Find the mac addresses
AMAC=$($SSH $A "/bin/cat /sys/class/net/eth0/address")
BMAC=$($SSH $B "/bin/cat /sys/class/net/eth0/address")

apxe=$(pxefy_mac $AMAC)
bpxe=$(pxefy_mac $BMAC)

# Create the files
create_pxe_file $apxe $A
create_pxe_file $bpxe $B

echo "Copying pxe files $apxe and $bpxe to the pxe server"
$SCP /tmp/$apxe root@pxesrv1:$PXE_PATH
$SCP /tmp/$bpxe root@pxesrv1:$PXE_PATH

stop_services

# Wipe disks on A and reboot
wipe_and_reboot $A

# Wait 15 mins for A to finish secerase etc.
echo "Waiting $HEADSTART sec for A to start install and initial steps"
countdown $HEADSTART

# Delete the pxe files to avoid accidental install
echo "Deleting pxe file $apxe for controller A"
$SSH pxesrv1 "/bin/rm -f $PXE_PATH/$apxe"
if [[ $? -ne 0 ]]; then
	echo "Unable to delete $PXE_PATH/$apxe on the pxe server 1. Needs manual delete to avoid accidental reinstall!!"
fi

# Wipe and reboot B
wipe_and_reboot $B

# Wait 15 mins before deleting pxe file
echo "Wait $HEADSTART sec to delete pxe file $bpxe for controller B"
countdown $HEADSTART

echo "Deleting pxe files $bpxe"
$SSH pxesrv1 "/bin/rm -f $PXE_PATH/$bpxe"
if [[ $? -ne 0 ]]; then
	echo "Unable to delete $PXE_PATH/$bpxe on the pxe server 1. Needs manual delete to avoid accidental reinstall!!"
fi

# Install should be in progress. Wait until we are able to ping the target
wait_until_up

if [[ -e /auto/e2e/bin/assimilate.py ]]; then
	echo "System is up. Assimilating"
	/auto/e2e/bin/assimilate.py --ignore_quarantined --ignore_owner --ignore_running $target
else
	echo "System is up. Run assimilate"
fi

