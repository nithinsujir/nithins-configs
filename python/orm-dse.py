#!/usr/bin/env python
import os
import pexpect
import optparse
import sys

parser = optparse.OptionParser()

(opts, args) = parser.parse_args()


HOST = '10.220.6.31'
LOGIN = 'a'
PASSWORD = 'a'
PROMPT = 'NE6.31'
ZPROMPT = 'qnx6.3.2'
DBIPROMPT = 'dbi->'

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


tel = Telnet()
SendExpect(tel, 'c1', ZPROMPT)
SendExpect(tel, 'dbiClient -n', DBIPROMPT)
SendExpect(tel, '@sd 0', DBIPROMPT)
SendExpect(tel, '@ss Mog-1', DBIPROMPT)


SendExpect(tel, 'uob SLOT 1-A-2 CircuitPackType=OAM CircuitPackStatus=PLUG_IN', DBIPROMPT)
SendExpect(tel, 'uob SLOT 1-A-2 CircuitPackStatus=INIT', DBIPROMPT)
SendExpect(tel, 'uob ORM 1-A-2 CoId=/CogOrm-1-2/ORM=1-A-2 InstalledEqptTyp=ORM_CXH1_MS CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob ORM 1-A-2 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob SLOT 1-A-3 CircuitPackType=OAM CircuitPackStatus=PLUG_IN', DBIPROMPT)
SendExpect(tel, 'uob SLOT 1-A-3 CircuitPackStatus=INIT', DBIPROMPT)
SendExpect(tel, 'uob ORM 1-A-3 CoId=/CogOrm-1-3/ORM=1-A-3 InstalledEqptTyp=ORM_CXH1_MS CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob ORM 1-A-3 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob DCFPTP 1-A-2-D1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob DCFPTP 1-A-2-D1 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob DCFPTP 1-A-3-D1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob DCFPTP 1-A-3-D1 CoControlStatus=READY', DBIPROMPT)

SendExpect(tel, '@ss Mog-2', DBIPROMPT)

SendExpect(tel, 'uob SLOT 2-A-2 CircuitPackType=OAM CircuitPackStatus=PLUG_IN', DBIPROMPT)
SendExpect(tel, 'uob SLOT 2-A-2 CircuitPackStatus=INIT', DBIPROMPT)
SendExpect(tel, 'uob DSE 2-A-2 CoId=/CogDse-2-2/DSE=2-A-2 InstalledEqptTyp=DSE_1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob SLOT 2-A-3 CircuitPackType=OAM CircuitPackStatus=PLUG_IN', DBIPROMPT)
SendExpect(tel, 'uob SLOT 2-A-3 CircuitPackStatus=INIT', DBIPROMPT)
SendExpect(tel, 'uob DSE 2-A-3 CoId=/CogDse-2-3/DSE=2-A-3 InstalledEqptTyp=DSE_1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob DSEPTP 2-A-2-D1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob DSEPTP 2-A-2-D1 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob DSEPTP 2-A-3-D1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob DCFPTP 2-A-3-D1 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob OSAPTP 2-A-2-A1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob OSAPTP 2-A-2-A1 CoControlStatus=READY', DBIPROMPT)
SendExpect(tel, 'uob OSAPTP 2-A-3-A1 CoControlStatus=SWINIT', DBIPROMPT)
SendExpect(tel, 'uob OSAPTP 2-A-3-A1 CoControlStatus=READY', DBIPROMPT)

