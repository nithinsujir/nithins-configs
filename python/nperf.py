#!/usr/bin/python
import pexpect
import optparse
import os
import re
import time
import sys

def spawn_ssh(target, login, passwd):
	child = pexpect.spawn('ssh -X ' + login + '@' + target)
	child.logfile_read = sys.stdout
	#child.expect('password:')
	#child.sendline(passwd)
	child.expect('>')

	return child

M1 = 'dl1'
M2 = 'hp2'
RUNLENGTH = '10'

# Parse command line options
parser = optparse.OptionParser()
parser.add_option('-i', '--ip', dest='ip', help='Ip address digit x for x.x.x.[12]')
parser.add_option('-l', '--loops', dest='loops', help='Number of loops')
(opts, args) = parser.parse_args()

if opts.ip:
	digit = opts.ip
else:
	digit = '1'

if opts.loops:
	loops = int(opts.loops)
else:
	loops = 1

	
l1 = spawn_ssh(M1, 'nsujir', 'f')
l2 = spawn_ssh(M1, 'nsujir', 'f')
l3 = spawn_ssh(M1, 'nsujir', 'f')

r1 = spawn_ssh(M2, 'nsujir', 'f')
#r2 = spawn_ssh(M2, 'nsujir', 'f')
#r3 = spawn_ssh(M2, 'nsujir', 'f')

ltotal = 0
rtotal = 0

for i in xrange(loops):
	l1.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.2 -l ' + RUNLENGTH)
	l2.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.2 -l ' + RUNLENGTH)
	l3.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.2 -l ' + RUNLENGTH)

	r1.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.1 -l ' + RUNLENGTH)
	#r2.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.1 -l ' + RUNLENGTH)
	#r3.sendline('/home/nsujir/bin/netperf -H ' + digit + '.' + digit + '.' + digit + '.1 -l ' + RUNLENGTH)

	l1.expect('>', timeout = 90)
	l2.expect('>', timeout = 90)
	l3.expect('>', timeout = 90)
	r1.expect('>', timeout = 90)
	#r2.expect('>', timeout = 90)
	#r3.expect('>', timeout = 90)

	re1 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', l1.before)
	ltotal = ltotal + float(re1.group(1))

	re2 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', l2.before)
	ltotal = ltotal + float(re2.group(1))

	re3 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', l3.before)
	ltotal = ltotal + float(re3.group(1))

	re4 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', r1.before)
	rtotal = rtotal + float(re4.group(1))

	#re5 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', r2.before)
	#rtotal = rtotal + float(re5.group(1))

	#re6 = re.search(RUNLENGTH + r'.\d\d\s+([\d\.]+)', r3.before)
	#rtotal = rtotal + float(re6.group(1))

	#print 'Throughput: ' + re1.group(1) + ' ' + re2.group(1)

print 'Avg throughput: Tx - %d Rx - %d Total - %d' % (ltotal/loops, rtotal/loops, (ltotal + rtotal)/loops)
