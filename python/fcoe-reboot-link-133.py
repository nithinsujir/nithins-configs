#!/usr/bin/python
import pexpect
import re
import time
import sys
import emailer
import os

TEST_SERVER = 'bh'
REBOOT_WAIT = 330
PROMPT = '122-133'

def countdown(line, wait_time):
    print '\n'
    for i in range(wait_time):
        print '%s: %2d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%20s\n' % ' '

ssh = pexpect.spawn('ssh ' + TEST_SERVER)
#ssh.logfile_read = sys.stdout
ssh.logfile = open('/tmp/' + TEST_SERVER + '.log', 'a')
ssh.expect(PROMPT)

def reboot(ssh):
	ssh.sendline('sudo reboot')
	countdown('Rebooting', REBOOT_WAIT)
	ssh = pexpect.spawn('ssh ' + TEST_SERVER)
        ssh.logfile_read = sys.stdout
	ssh.logfile = open('/tmp/' + TEST_SERVER + '.log', 'a')
	ssh.expect(PROMPT)

	return ssh

def reload(ssh):
	ssh.sendline('sudo fcoeadm -d eth4')
	ssh.expect(PROMPT)
	ssh.sendline('sudo fcoeadm -d eth5')
	ssh.expect(PROMPT)
	ssh.sendline('sudo modprobe -r bnx2fc')
	ssh.expect(PROMPT)
	ssh.sendline('sudo modprobe -r fcoe')
	ssh.expect(PROMPT)
	ssh.sendline('sudo service fcoe stop')
	ssh.expect(PROMPT)
	ssh.sendline('fcoeadm -i')
	ssh.expect('No FCoE interfaces created')
	ssh.sendline('sudo service fcoe start')
	ssh.expect(PROMPT)
	time.sleep(10)

for i in xrange(0, 99999):
	print '\n---------------[ Iteration: %d ]-----------------' % i
	ssh.sendline('fcoeadm -i eth4.4-fcoe')
	ssh.expect('Online')
	ssh.sendline('fcoeadm -i eth5.4-fcoe')
	ssh.expect('Online')

	ssh = reboot(ssh)


