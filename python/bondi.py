#!/usr/bin/env python
import pexpect
import sys
import time

SSH='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o loglevel=error'

def countdown(line, wait_time):
    print ''
    for i in range(wait_time):
        print '%s: %3d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%80s\r' % ' '

def _ssh(server):
    ssh = pexpect.spawn(SSH + ' ' + server + ' -l root')
    ssh.logfile = sys.stdout

    rc = ssh.expect(['#', '\$', 'password:', 'RSA key fingerprint'])

    if rc == 0 or rc == 1:
        pass
    else:
        if rc == 3:
            ssh.sendline('yes')
            ssh.expect(['Password:', 'password:'])

        ssh.sendline(password)
        ssh.expect(['#', '\$'])

    return ssh


if len(sys.argv) < 2:
	sys.exit(sys.argv[0] + ' <server> [password]')

server = sys.argv[1]

password = 'tintri99'
if len(sys.argv) > 2:
	password = sys.argv[2]

ssha = _ssh(server + 'a')
sshb = _ssh(server + 'b')

ssha.sendline('hamoncmd')
rc = ssha.expect(['REDUNDANT', 'UNAVAILABLE'], timeout = 5)
if rc == 1:
    ssha.sendline('service txos start')
    ssha.expect(server + '#a')

    countdown('Wait a bit for A to come up', 10)
    ssha.sendline('hamoncmd')
    ssha.expect(server + '#a')

# If main ip prompt is not #a, failover
try:
    ssh = _ssh(server)
    ssh.sendline('ls')
    ssh.expect(server + '#a', timeout = 5)
except:
    # A is secondary. Do a failover
    ssha.sendline('hamoncmd -O')
    ssha.expect(server + '#a')
    time.sleep(30)
    ssha.sendline('hamoncmd')
    ssha.expect(server + '#a', timeout = 60)

ssha.sendline('ifdown bondinternal0')
ssha.expect(server + '#a')

# Stop hamon and txos. First secondary, then primary
sshb.sendline('service hamon stop')
sshb.expect(server + '#b')

sshb.sendline('service txos stop')
sshb.expect(server + '#b')

ssha.sendline('service hamon stop')
ssha.expect(server + '#a')

ssha.sendline('service txos stop')
ssha.expect(server + '#a')

time.sleep(5)

# Bring txos up on A
ssha.sendline('service hamon start')
ssha.expect(server + '#a')

ssha.sendline('service txos start')
ssha.expect(server + '#a')

# Wait until A becomes PRIMARY to start B. Else, B will shoot A
time.sleep(15)

#ssha.sendline('hamoncmd')
#ssha.expect('PRIMARY')

sshb.sendline('service hamon start')
sshb.expect(server + '#b')

sshb.sendline('service txos start')
sshb.expect(server + '#b')

ssha.sendline('ifup bondinternal0')
ssha.expect(server + '#a')

countdown('Allow a little while for B to come up', 70)
ssha.sendline('hamoncmd')
ssha.expect('REDUNDANT')

ssha.sendline('service txos stop')
ssha.expect(server + '#a')

ssha.sendline('ifconfig')
ssha.expect(server + '#a')

