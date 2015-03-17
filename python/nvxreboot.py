#!/usr/bin/env python
import pexpect
import sys
import time

REBOOT_WAIT = 300
SSH_RETRY_WAIT = 30
RAND_WAIT = 20

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
    except:
        if retried < 5:
            pass
            countdown('Unable to connect. Retrying in', SSH_RETRY_WAIT)
            retried = retried + 1
            continue
        else:
            print 'Cannot connect. Exiting...'

    # Check the contents 2nd iteration onwards
    if i > 0:
        ssh.sendline('dd if=/dev/umema1 of=/var/corefiles/cur-umem.bin bs=1M count=100')
        ssh.expect('#')
        ssh.sendline('diff -s /var/corefiles/prev-umem.bin /var/corefiles/cur-umem.bin')
        ssh.expect('identical')

    # Randomize nvram and save the file
    ssh.sendline('dd if=/dev/urandom of=/dev/umema1 bs=1M count=100')
    countdown('Waiting for initialization', RAND_WAIT)
    ssh.expect('#')
    ssh.sendline('dd if=/dev/umema1 of=/var/corefiles/prev-umem.bin bs=1M count=100')
    ssh.expect('#')
    ssh.sendline('sync')
    ssh.expect('#')

    ssh.sendline('reboot')
    countdown('Waiting for reboot', REBOOT_WAIT)

    i = i + 1

