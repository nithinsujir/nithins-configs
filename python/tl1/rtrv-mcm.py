#!/usr/bin/python
import pexpect
import optparse
import os
import re
import time
import sys
import shutil

parser = optparse.OptionParser()
parser.add_option('-i', '--ip', dest='ip', help='Target Ip')

(opts, args) = parser.parse_args()

TARGET_IP = '34.45.56.1'
if opts.ip:
    TARGET_IP = opts.ip
    if not re.match('\d+\.\d+\.\d+\.\d+', TARGET_IP):
        TARGET_IP = '10.220.16.' + opts.ip


def spawn_tl1():
    child = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
    child.logfile_read = sys.stdout
    child.expect('TL1>>')
    child.sendline('act-user::secadmin:c::infinera1;')
    child.expect('Your password')

    return child

tl1 = spawn_tl1()

# Add Shelf Chassis
while True:
    tl1.send('rtrv-eqpt:::c::mcm;')
    tl1.expect(['COMPLD', 'DENY'])

tl1.sendline('canc-user::secadmin:c;')

