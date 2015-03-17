#!/usr/bin/env python
# Update hosts file with connected chassis.
import os
import pexpect
import shutil
import hashlib

PORT = '3632'
TIMEOUT = 2
TMP_HOSTS = '/tmp/hosts'
HOSTS = '/home/nsujir/.distcc/hosts'
ALLHOSTS = '/home/nsujir/.distcc/allhosts'

fil = open(ALLHOSTS, 'r')
hosts = fil.readline().split()
fil.close()

connected = []

for host in hosts:
    try:
        tel = pexpect.spawn('telnet ' + host + ' ' + PORT, timeout = TIMEOUT)
        tel.expect('Connected')
        print 'Connected: ' + host
        connected.append(host)
    except:
        print '                         Disconnected: ' + host


# Write new hosts file
fil = open(TMP_HOSTS, 'w')
fil.write('localhost/3\n')
fil.write('10.220.0.60/8\n')
for host in connected:
    fil.write(host + '\n')
fil.close()

# Compare digest with old hosts file
dnew = hashlib.md5(open(TMP_HOSTS, 'r').read()).hexdigest()
dold = hashlib.md5(open(HOSTS, 'r').read()).hexdigest()

if dold != dnew:
    print 'Files differ. Copying'
    shutil.copy(TMP_HOSTS, HOSTS)
else:
    print 'No change in hosts'
