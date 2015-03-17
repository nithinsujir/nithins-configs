import optparse
import sys
import time
import pexpect
import sys
from telnet import telnet

TIMEOUT = 1800
REBOOT_WAIT = 30

# Constants
NE = '10.220.16.181'
LOGIN= 'root'
PASSWD = 'infinera1'

i = 0
while True:
    try:
        tel = telnet(NE, LOGIN, PASSWD, '#')
        tel.run('sloginfo -w')
        tel.interact()
    except:
        print 'Waiting %d secs for reboot' % REBOOT_WAIT
        time.sleep(REBOOT_WAIT)
        i = i + 1
        pass


