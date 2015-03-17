#!/usr/bin/python
import pexpect
import optparse
import sys


ssh = pexpect.spawn('ssh 10.13.243.115 -l root')
ssh.expect('password:')
ssh.sendline('br0adc0m$')
ssh.expect('>')
ssh.sendline('reset system1')
