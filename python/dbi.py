#!/usr/bin/env python
import os
import pexpect
import optparse
import sys

parser = optparse.OptionParser()
parser.add_option('-m', '--max', dest='max', help='Max zhosts')

(opts, args) = parser.parse_args()


HOST = '10.220.6.31'
LOGIN = 'a'
PASSWORD = 'a'
PROMPT = 'NE6.31'
ZPROMPT = 'qnx6.3.2'
DBIPROMPT = 'dbi->'

MAX_ZHOST = 1
if opts.max:
    MAX_ZHOST = int(opts.max)


dbivals = {
    'thcomponent':'1',
    'dth':'1',
    'dh':'1',
    'all':'1'
}


def Telnet():
    tel = pexpect.spawn('/usr/bin/telnet ' + HOST)
    tel.logfile = sys.stdout
    tel.expect('login:')
    tel.sendline(LOGIN)
    tel.expect('Password:')
    tel.sendline(PASSWORD)
    tel.expect(PROMPT)

    return tel

def SendExpect(tel, send, expect):
    tel.sendline(send)
    tel.expect(expect)


def ApplyDbiVals(tel, server):
    SendExpect(tel, '@ss ' + server, DBIPROMPT)

    for k, v in dbivals.items():
        SendExpect(tel, 'strl ' + k + ' ' + v, DBIPROMPT)


tel = Telnet()
SendExpect(tel, 'c1', ZPROMPT)
SendExpect(tel, 'dbiClient -n', DBIPROMPT)
SendExpect(tel, '@sd 0', DBIPROMPT)
ApplyDbiVals(tel, 'Cmog')

for i in range(1, MAX_ZHOST + 1):
    ApplyDbiVals(tel, 'Mog-' + str(i))

SendExpect(tel, '@exit', ZPROMPT)
