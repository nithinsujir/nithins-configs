#!/usr/bin/env python
import pexpect
import sys
import time

REBOOT_WAIT = 10
ADJCOUNT = 20
ADJTIMEX_WAIT = ADJCOUNT * 10

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

i = 1
while True:
    print 'Iteration: %d' % i

    try:
        ssh = pexpect.spawn('ssh ' + server + ' -l root')
        ssh.logfile = sys.stdout

        rc = ssh.expect(['#', '\$', 'password:', 'RSA key fingerprint'], timeout = 120)

        if rc == 3:
                ssh.sendline('yes')
                ssh.expect(['Password:', 'password:'])

        ssh.sendline(password)
        ssh.expect(['#', '\$'])
    except:
        pass
        countdown('Unable to connect. Retrying in', REBOOT_WAIT)
        continue

    ssh.sendline('adjtimex -p')
    ssh.expect('#')
    ssh.sendline('adjtimex -c')
    countdown('Waiting for adjtimex', 70)
    ssh.expect('#')
    ssh.sendline("./adjtimex.sh " + str(ADJCOUNT))
    countdown('Waiting for adjtimex', ADJTIMEX_WAIT)
    ssh.expect(['998', '999', '1000', '1001'])

    ssh.sendline('sync')
    ssh.sendline('reboot')

    countdown('Waiting for reboot', REBOOT_WAIT)
    i = i + 1

