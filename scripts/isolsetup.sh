#!/bin/bash
IPADDR=$1

if [[ -z $IPADDR ]]; then
	echo "Need ipmi ip"
	exit 1
fi

syscfg /bcs "MuffinMan" "Console Redirection" 1

ipmitool lan set 1 ipsrc static
ipmitool lan set 1 ipaddr $IPADDR
ipmitool lan set 1 netmask 255.255.0.0
ipmitool lan set 1 defgw ipaddr 10.40.0.1
ipmitool lan set 1 vlan id off
ipmitool lan set 1 access on
# This next one seems to fail if user is already named admin.
ipmitool user set name 3 admin
ipmitool user set password 3 tintri99
# privilege 3 = operator level
ipmitool user priv 3 4 1
ipmitool user enable 3

sed -i 's/^LogFile=.*$/exit 0/' /usr/local/tintri/bin/set_bmclan
