import pexpect
import sys

class expect:
    DEFAULT_TIMEOUT = 30

    def __init__(self, cmd, dum=None, dums=None):
        self.session = pexpect.spawn(cmd, logfile = sys.stdout)

    def expect(self, expect_string, time_out = DEFAULT_TIMEOUT):
        self.session.expect(expect_string, timeout = time_out)

    def sendline(self, send_string):
        self.session.sendline(send_string)

    def send_expect(self, send_string, expect_string, time_out = None):
        self.sendline(send_string)
        self.expect(expect_string, time_out)

    def interact(self):
        self.session.logfile = None
        self.session.logfile_read = sys.stdout
        self.session.interact()

