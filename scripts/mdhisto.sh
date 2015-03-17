#!/bin/bash
log=$1

# Partition end in sectors
root_end=16777279
log_end=243269696
pgsql_end=285212745
core_end=1019215946

root_io=0
log_io=0
pgsql_io=0
core_io=0

for lba in $(grep -v "\[" $log | grep "\+" | grep W | awk {'print $8'}); do
	if [[ $lba -le $root_end ]]; then
		((root_io++))
	elif [[ $lba -le $log_end ]]; then
		((log_io++))
	elif [[ $lba -le $pgsql_end ]]; then
		((pgsql_io++))
	elif [[ $lba -le $core_end ]]; then
		((core_io++))
	fi
done

echo "root_io	: $root_io"
echo "log_io	: $log_io"
echo "pgsql_io	: $pgsql_io"
echo "core_io	: $core_io"
