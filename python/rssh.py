#!/usr/bin/python
import pexpect
import sys

if len(sys.argv) < 2:
	sys.exit(sys.argv[0] + ' <server> [password]')

server = sys.argv[1]

password = 'password'
if len(sys.argv) > 2:
	password = sys.argv[2]

ssh = pexpect.spawn('ssh ' + server + ' -l root', timeout = 60)

rc = ssh.expect(['#', '\$', 'password:', 'RSA key fingerprint'])

if rc == 0:
    ssh.interact()

if rc == 3:
	ssh.sendline('yes')
	ssh.expect(['Password:', 'password:'])

ssh.sendline(password)
ssh.expect(['#', '\$'])
ssh.sendline()
ssh.interact()
