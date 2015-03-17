#!/usr/bin/env python
import pexpect
import sys
import time

SSH_RETRIES = 20
STAT_WAIT = 3600

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
    except:
        if retried < SSH_RETRIES:
            pass
            retried = retried + 1
            time.sleep(1)
            continue

    retried = 0

    ssh.sendline('date')
    ssh.expect('#')
    ssh.sendline('uptime')
    ssh.expect('#')
    ssh.sendline('iostat -m /dev/md0')
    ssh.expect('#')

    time.sleep(STAT_WAIT)
