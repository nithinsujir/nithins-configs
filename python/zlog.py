#!/usr/bin/env python
import os
import pexpect
import sys
import optparse
import time

usage = '%prog <zhostid>'
parser = optparse.OptionParser(usage = usage)

(opts, args) = parser.parse_args()

HOST = '10.220.6.31'
LOGIN = 'a'
PASSWORD = 'a'
PROMPT = 'NE6.31'
ZPROMPT = 'qnx6.3.2'
BOOT_WAIT = 20
ARG_COUNT = 1

def Telnet():
    tel = pexpect.spawn('/usr/bin/telnet ' + HOST)
    tel.logfile_read = sys.stdout
    return tel

def Login(tel):
    tel.expect('login:')
    tel.sendline(LOGIN)

def Password(tel):
    tel.expect('Password:')
    tel.sendline(PASSWORD)

    return tel

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

tel = Telnet()
Login(tel)
Password(tel)
tel.expect(PROMPT)
tel.sendline('sl' + args[0])
tel.interact()
