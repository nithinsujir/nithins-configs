#!/usr/bin/env bash
SSH="ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error"

#mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Ubuntu\ Mono -xftsz 14 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Ubuntu\ Mono -xftpsz 9 -geometry 210x60 -at -e ssh -Y nsujir-ws
mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Inconsolata -xftsz 14 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Ubuntu\ Mono -xftpsz 9 -geometry 210x60 -at -e $SSH -Y nsujir-ws
#mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Liberation\ Mono -xftsz 11 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Ubuntu\ Mono -xftpsz 9 -geometry 80x30
#mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Monospace -xftsz 10 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Monospace -xftpsz 8
#mrxvt +bt -bg beige  -fg black -xft -xftaa -xftfn Fira\ Mono -xftsz 10 -aht -hb -sr -wd /home/nsujir -cf /home/nsujir/.mrxvtrc -sl 9999 -itabbg grey -itabfg black -hold 0 +showmenu -mvt 15 -xftpfn Ubuntu\ Mono -xftpsz 9 -geometry 80x30
