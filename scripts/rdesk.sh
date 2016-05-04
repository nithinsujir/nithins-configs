#!/usr/bin/env bash
res=$(xdpyinfo  | grep dimensions | awk {'print $2;'})
echo $res

if [[ $res =~ 1600x900 ]]; then
	res=1600x840
elif [[ $res =~ 1366x768 ]]; then
	res=1366x700
else
	res=1900x1050
fi

passwd=$(zenity --password --title=Authentication)
rdesktop -g $res -u tintri\\nsujir -p $passwd nsujir-win -K -x 0x80
