#!/usr/bin/python
import pexpect
import re
import time
import sys
import emailer
import os

TEST_SERVER = 'hp2'
REBOOT_WAIT = 150

def countdown(line, wait_time):
    print '\n'
    for i in range(wait_time):
        print '%s: %2d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%20s\n' % ' '

for i in xrange(0, 99999):
	print '\n---------------[ Iteration: %d ]-----------------' % i
	ssh = pexpect.spawn('ssh ' + TEST_SERVER)
	#ssh.logfile_read = sys.stdout
	ssh.logfile = open('/tmp/' + TEST_SERVER + '.log', 'a')
	ssh.expect('hp2')
	ssh.sendline('fcoeadm -i')
	ssh.expect('Online')
	ssh.sendline('sudo reboot')
	countdown('Rebooting', REBOOT_WAIT)

