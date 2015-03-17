#!/usr/bin/python
import os
import pexpect
import sys
import optparse
import time

parser = optparse.OptionParser()
parser.add_option('-m', '--max', dest='max', help='Max zhosts')
parser.add_option('-i', '--ip', dest='ip', help='x86 ip')
parser.add_option('-l', '--login', dest='login', help='login')
parser.add_option('-p', '--password', dest='password', help='password')
parser.add_option('-t', '--prompt', dest='prompt', help='prompt')
parser.add_option('-z', '--zprompt', dest='zprompt', help='zprompt')

(opts, args) = parser.parse_args()

HOST = '10.220.6.31'
LOGIN = 'a'
PASSWORD = 'a'
PROMPT = 'NE6.31'
ZPROMPT = 'qnx6.3.2'
BOOT_WAIT = 20

MAX_ZHOST = 2
if opts.max:
    MAX_ZHOST = int(opts.max)

if opts.ip:
    HOST = opts.ip

if opts.login:
    LOGIN = opts.login

if opts.password:
    PASSWORD = opts.password

if opts.prompt:
    PROMPT = opts.prompt

if opts.zprompt:
    ZPROMPT = opts.zprompt

INFINITE_WAIT = 999999

tel = {}

def Telnet():
    tel = pexpect.spawn('/usr/bin/telnet ' + HOST)
    tel.logfile = sys.stdout
    return tel

def Login(tel):
    tel.expect('login:')
    tel.sendline(LOGIN)

def Password(tel):
    tel.expect('Password:')
    tel.sendline(PASSWORD)

    return tel

def countdown(line, wait_time):
    print '\n'
    for i in range(wait_time):
        print '%s: %2d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%40s\n' % ' '

# Kill hosts
for i in xrange(MAX_ZHOST):
    tel[i] = Telnet()
for i in xrange(MAX_ZHOST):
    Login(tel[i])
for i in xrange(MAX_ZHOST):
    Password(tel[i])
for i in xrange(MAX_ZHOST):
    tel[i].expect(PROMPT)

for i in xrange(MAX_ZHOST):
    tel[i].sendline('zshut zhost' + str(i + 1))

# Wait for kill complete
for i in xrange(MAX_ZHOST):
    tel[i].expect(PROMPT)

tel[0].sendline('zps zhost1')
tel[0].expect(PROMPT)
tel[0].sendline('zps zhost2')
tel[0].expect(PROMPT)
tel[0].sendline('zps zhost3')
tel[0].expect(PROMPT)
tel[0].sendline('zps zhost4')
tel[0].expect(PROMPT)

# Connect again so the interfaces are generated
for i in xrange(MAX_ZHOST):
    tel[i].sendline('zconnect zhost' + str(i + 1))
for i in xrange(MAX_ZHOST):
    tel[i].expect(ZPROMPT)
for i in xrange(MAX_ZHOST):
    tel[i].sendline('exit')
for i in xrange(MAX_ZHOST):
    tel[i].expect(PROMPT)



# Delete all cables
atel = Telnet()
Login(atel)
Password(atel)
atel.sendline('zdelconn -f -d -n -s')
atel.expect(PROMPT)

# Connect dcn
atel.sendline('zconnectdcn -z zhost1')
atel.expect(PROMPT)


if MAX_ZHOST > 1:
    # Connect nct
    nct_command = 'zconnectnct -z zhost1 '

    for i in range(1, MAX_ZHOST):
        nct_command = nct_command + ' zhost' + str(i + 1)

    atel.sendline(nct_command)
    atel.expect(PROMPT)

# Boot the hosts
for i in xrange(MAX_ZHOST):
    tel[i].sendline('zbootzhost zhost' + str(i + 1))
    tel[i].expect(PROMPT, timeout = INFINITE_WAIT)
    countdown('Waiting for boot', BOOT_WAIT)


