#!/bin/bash
IPADDR=$1
GW=$2

if [[ -z $IPADDR || -z $GW ]]; then
	echo "Need ipmi ip and gw"
	exit 1
fi

/usr/local/tintri/bin/syscfg /bcs "MuffinMan" "Console Redirection" 1

ipmitool lan set 1 ipsrc static
ipmitool lan set 1 ipaddr $IPADDR
ipmitool lan set 1 netmask 255.255.0.0
ipmitool lan set 1 defgw ipaddr $GW
ipmitool lan set 1 vlan id off
ipmitool lan set 1 access on
# This next one seems to fail if user is already named admin.
ipmitool user set name 3 admin
ipmitool user set password 3 password
# privilege 3 = operator level
ipmitool user priv 3 4 1
ipmitool user enable 3

sed -i 's/^LogFile=.*$/exit 0/' /usr/local/tintri/bin/set_bmclan
