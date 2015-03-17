#!/bin/bash

echo $1
{
cat << 'EOF'
# This is a generated cfg file
ONBOOT=yes
NM_CONTROLLED=no
BOOTPROTO=static
DEVICE=$1
EOF
} > /tmp/$1.cfg
