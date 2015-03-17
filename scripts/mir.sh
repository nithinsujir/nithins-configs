#!/bin/bash
set -x


TbinDir=/usr/local/tintri/bin
Rcmd="/usr/bin/ssh tt-peer-controller."

/usr/local/tintri/bin/inst_nvram
$Rcmd /usr/local/tintri/bin/inst_nvram

$TbinDir/nvmir -p 55555 -l tt-this-controller. -r tt-peer-controller. > /dev/null 2>&1 &
$Rcmd $TbinDir/nvmir -p 55555 -l tt-this-controller. -r tt-peer-controller.  > /dev/null 2>&1 &

