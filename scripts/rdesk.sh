#!/usr/bin/env bash
passwd=$(zenity --password --title=Authentication)
rdesktop -g 1900x1050 -u tintri\\nsujir -p $passwd nsujir-win -K -x 0x80
