#!/usr/bin/python
import os
import pexpect
import sys
import optparse
import re
import failmail
import time

PASSWORD=''

def send_expect(sess, line, prompt, timeout_ = 60):
	sess.sendline(line)
	sess.timeout = timeout_
	sess.expect(prompt)

def spawn_ssh(target):
	child = pexpect.spawn('ssh root@' + target, timeout = 60)
	child.logfile_read = sys.stdout

	index = child.expect(['assword:', 'continue'])

	if index == 1:
		print 'send yes'
		send_expect(child, 'yes', 'password')

	send_expect(child, PASSWORD, '#')

	return child

ses = spawn_ssh('10.13.127.123')

vmmap = {}

for i in xrange(99999999):
	for vmnic in ['vmnic2', 'vmnic6']:
		send_expect(ses, 'ethtool -S ' + vmnic + ' | grep dbg | grep tso', '#')
		lines = ses.before + ses.after

		m = re.search('check_1: (.*)', lines, re.MULTILINE)
		
		if m:
			print 'Count: ' + m.group(1)
			if i == 0:
				vmmap[vmnic] = int(m.group(1))

			if int(m.group(1)) != vmmap[vmnic]:
				line = 'Cross count updated on ' + vmnic + 'from ' + str(vmmap[vmnic]) + ' to ' + m.group(1)
				failmail.send_fail(['nsujir@broadcom.com', 'huangjw@broadcom.com', 'anilgv@broadcom.com'], line)
				vmmap[vmnic] = int(m.group(1))
		else:
			print 'No match'

	time.sleep(1)

