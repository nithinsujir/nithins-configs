#!/bin/bash
IPADDR=$1

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
ipmitool user priv 3 3 1
ipmitool user enable 3

