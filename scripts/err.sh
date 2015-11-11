#!/bin/bash
echo "add tgt-id=1 opcode=28 lba=1000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject

echo "add tgt-id=2 opcode=28 lba=2000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=3 opcode=28 lba=3000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=2 opcode=28 lba=4000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=1 opcode=28 lba=5000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=3 opcode=28 lba=6000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=1 opcode=28 lba=7000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=2 opcode=28 lba=8000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=3 opcode=28 lba=9000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=1 opcode=28 lba=10000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
echo "add tgt-id=2 opcode=28 lba=11000 len=2 mode=return count=9999999 prob=100 result=2 key=6 asc=29 ascq=3 fixable" > /sys/class/scsi_host/host6/error_inject
