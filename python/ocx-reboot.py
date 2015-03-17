#!/usr/bin/python
import pexpect
import re
import time
import sys
import emailer
import os


ssh = pexpect.spawn('ssh lg')
ssh.logfile_read = sys.stdout
ssh.expect('>')
ssh.sendline('ssh dkms-bld')
ssh.expect('Password')
ssh.sendline('f')
ssh.expect('dkms')
ssh.sendline('su')
ssh.expect('Password')
ssh.sendline('linux1')


