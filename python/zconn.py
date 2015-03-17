import os
import pexpect
import sys

HOST = '10.220.6.31'
LOGIN = 'a'
PASSWORD = 'a'

tel = pexpect.spawn('/usr/bin/telnet ' + HOST)
tel.logfile = sys.stdout
tel.expect('login:')
tel.sendline(LOGIN)
tel.expect('Password:')
tel.sendline(PASSWORD)
tel.expect(r'\$')
tel.sendline('zconnect zhost1')
tel.expect(r'\$')
tel.sendline('zconnectnet')
tel.expect(r'\$')
