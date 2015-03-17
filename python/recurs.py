import optparse
import sys
import time
import pexpect
import sys

TIMEOUT = 1800
REBOOT_WAIT = 200
f = open("/tmp/recurs.out", 'w')

def countdown(line, wait_time):
    for i in range(wait_time):
        print '%s: %3d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%80s\r' % ' '


def Print(lin):
    print lin
    sys.stdout.flush()

class expect:
    DEFAULT_TIMEOUT = 30

    def __init__(self, cmd, dum=None, dums=None):
        self.session = pexpect.spawn(cmd, logfile = f, timeout = TIMEOUT)

    def expect(self, expect_string, time_out = DEFAULT_TIMEOUT):
        return self.session.expect(expect_string, timeout = time_out)

    def sendline(self, send_string):
        self.session.sendline(send_string)

    def send_expect(self, send_string, expect_string, time_out = None):
        self.sendline(send_string)
        self.expect(expect_string, time_out)

    def interact(self):
        self.session.logfile = None
        self.session.logfile_read = sys.stdout
        self.session.interact()


class telnet(expect):
    def __init__(self, ipaddr, login, password, prompt = '>'):
        self.TELNET_PROMPT = prompt

        expect.__init__(self, 'telnet ' + ipaddr)
        expect.expect(self, 'login:', TIMEOUT)
        expect.send_expect(self, login, 'Password')
        expect.send_expect(self, password, self.TELNET_PROMPT)


    def run(self, cmd):
        expect.send_expect(self, cmd, self.TELNET_PROMPT)

# Constants
NE = '10.220.16.181'
LOGIN= 'root'
PASSWD = 'infinera1'

# Read arguments
Print('Connecting to NE: ' + NE)

for x in range(1,100):
    rval = 0
    Print('Trying to telnet...')
    ub = telnet(NE, LOGIN, PASSWD, '#')
    try:
        Print('Waiting for management interfaces')
        ub.sendline('sloginfo -w')
        rval = ub.expect(['Opening the management interface', 'failed to send', 'SIGSEGV'], TIMEOUT)
        #print rval
    except:
        Print(str(x) + ' : Failed')
    
    try:
        if rval == 0:
            ub = telnet(NE, LOGIN, PASSWD, '#')
            Print(str(x) + ' : Success')
        elif rval == 1:
            Print(str(x) + ' : Failed to send')
        elif rval == 2:
            Print(str(x) + ' : SIGSEGV')
        else:
            Print('rval =' + str(rval))
    except:
        Print('Unable to telnet. Probably already rebooting')
        pass

    Print('Rebooting...')
    ub.sendline('reboot')
    countdown('Waiting for telnet server to be available', REBOOT_WAIT)
