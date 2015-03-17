#!/usr/bin/python
import pexpect
import optparse
import os
import re
import time
import sys

LOGIN ='root'
PASSWORD ='bcom'
TARGET = 'bh'

def spawn_ssh():
	child = pexpect.spawn('ssh -X ' + LOGIN + '@' + TARGET)
	child.logfile_read = sys.stdout
	child.expect('password:')
	child.sendline(PASSWORD)

	return child

# Parse command line options
parser = optparse.OptionParser()
parser.add_option('-t', '--target', dest='target', help='Machine Name or Ip address')
parser.add_option('-l', '--login', dest='login', help='Login')
parser.add_option('-p', '--password', dest='password', help='Password')

(opts, args) = parser.parse_args()

if opts.target:
	TARGET = opts.target

if opts.login:
	LOGIN = opts.login

if opts.password:
	PASSWORD = opts.password



child = spawn_ssh()
child.interact()
