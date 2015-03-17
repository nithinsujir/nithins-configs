#!/usr/bin/env python
import pexpect
import sys
import time

REBOOT_WAIT = 300
SSH_RETRY_WAIT = 30

def countdown(line, wait_time):
    for i in range(wait_time):
        print '%s: %3d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%80s\r' % ' '

if len(sys.argv) < 2:
	sys.exit(sys.argv[0] + ' <server> [password]')

server = sys.argv[1]

password = 'tintri99'
if len(sys.argv) > 2:
	password = sys.argv[2]

i = 0
retried = 0
while True:
    print 'Iteration: %d' % i

    try:
        ssh = pexpect.spawn('ssh ' + server + ' -l root')
        ssh.logfile = sys.stdout

        rc = ssh.expect(['#', '\$', 'password:', 'RSA key fingerprint'], timeout = 120)

        if rc == 0 or rc == 1:
            pass
        else:
            if rc == 3:
                ssh.sendline('yes')
                ssh.expect(['Password:', 'password:'])

            ssh.sendline(password)
            ssh.expect(['#', '\$'])

        ssh.sendline('HAMonCmd')
        ssh.expect('SYNCED')
    except:
        if retried < 5:
            pass
            countdown('Unable to connect. Retrying in', SSH_RETRY_WAIT)
            retried = retried + 1
            continue
        else:
            print 'Cannot connect. Exiting...'

    ssh.sendline('reboot')
    countdown('Waiting for reboot', REBOOT_WAIT)

    i = i + 1

