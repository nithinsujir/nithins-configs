#!/usr/bin/python
import pexpect
import optparse
import os
import re
import time
import sys
import shutil

parser = optparse.OptionParser()
parser.add_option('-m', '--mask', dest='mask', help='0 indexed chassis mask in hex. E.g. chassis 1 and 3 would be 0xa')
parser.add_option('-i', '--ip', dest='ip', help='Target Ip')

(opts, args) = parser.parse_args()

TARGET_IP = '34.45.56.1'
if opts.ip:
    TARGET_IP = opts.ip
    if not re.match('\d+\.\d+\.\d+\.\d+', TARGET_IP):
        TARGET_IP = '10.220.16.' + opts.ip


CHASSIS_MASK = 2
if opts.mask:
    if int(opts.mask, 16) & 1:
        print 'Mask bit 0 is set. Chassis bits should start from 1'
        sys.exit(1)

    CHASSIS_MASK = int(opts.mask, 16)
else:
    print 'No mask given. Assuming only chassis 1'

DLM_START = 3
DLM_END = 7
TAM_START = 1
TAM_END = 6
TOM_START = 1
TOM_END = 5

CHASSIS_SERIAL = 'NE631ZH0'

def spawn_tl1():
    child = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
    child.logfile_read = sys.stdout
    child.expect('TL1>>')
    child.sendline('act-user::secadmin:c::infinera1;')
    child.expect('Your password')

    return child

chassis_list = []

mask = CHASSIS_MASK
index = 0
while mask != 0:
    if (mask & 0x1) != 0:
        chassis_list.append(index)

    index = index + 1
    mask = mask >> 1

print 'Chassis list: ',
print chassis_list


tl1 = spawn_tl1()

# Add Shelf Chassis
while True:
    for chassis in chassis_list:
        tl1.sendline('ed-eqpt::' + str(chassis) + '-a-7a:c:::label=x;')
        tl1.expect(['COMPLD', 'DENY'])
        tl1.sendline('ed-eqpt::' + str(chassis) + '-a-7a:c:::label=y;')
        tl1.expect(['COMPLD', 'DENY'])

tl1.sendline('canc-user::secadmin:c;')

