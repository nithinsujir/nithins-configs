#!/bin/bash
. /usr/local/tintri/bin/cmn_funcs

/usr/local/tintri/bin/product-model | grep DN
if [[ $? -eq 0 ]]; then
	model=$OK
else
	model=$NOTOK
fi

pm=$(GetPlatformModel)
if [[ $? -ne 0 ]]; then
	echo "Unable to get platform model"
	exit 1
fi

if [[ $pm == "DN1" ]]; then
	mdsize=180354816
else
	mdsize=195034880
fi
bootsize=7824518
ddomsize=1048576

md=ok
idom=ok
ddom=ok
/bin/grep '$mdsize md0' /proc/partitions
if [[ $? -ne 0 ]]; then
	md=$NOTOK
fi

/bin/grep '$bootsize sdb1' /proc/partitions
if [[ $? -ne 0 ]]; then
	idom=$NOTOK
fi

/bin/grep '$ddomsize sda1' /proc/partitions
if [[ $? -ne 0 ]]; then
	ddom=$NOTOK
fi

numrd=$(/usr/local/tintri/bin/list_disks -R | wc -l)
echo "Num rdisks: $numrd"

rdisks=($(/usr/local/tintri/bin/list_disks -R))
for rd in ${rdisks[@]}; do
	echo $rd
	/usr/local/tintri/bin/disksig -r $rd | grep -e ctrlid -e MD -e model -e uuid
done

for rd in ${rdisks[@]}; do
	echo -n "$rd: "

	bpart=$(GetBootPart $rd)
	if [[ $? -ne 0 ]]; then
		echo "Unable to get bootpart"
		continue
	fi

	/bin/mkdir -p /rdboot
	/bin/mount ${rd}${bpart} /rdboot
	/bin/cat /rdboot/grub/grub.conf | grep kernel
	/bin/umount /rdboot
done

idisk=$(/usr/local/tintri/bin/list_disks -i)
/bin/mkdir -p /dom
/bin/mount ${idisk}1 /dom
echo -n "${idisk}: "
/bin/grep kernel /dom/grub/grub.conf
/bin/umount /dom

