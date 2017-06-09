#!/usr/bin/env bash
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"

mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Inconsolata -xftsz 12 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Ubuntu\ Mono -xftpsz 9 -geometry 80x30 -at -e $SSH -Y nsujir-ws
