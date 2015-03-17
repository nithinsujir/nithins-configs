from telnet import telnet
import optparse
import sys

# Constants
ARG_COUNT = 1
UBUNTU = '10.220.1.18'
UBUNTU_LOGIN = 'infinera'
UBUNTU_PASSWORD = 'infinera2'
CSIM_LOGIN = 'autotest'
CSIM_PASSWD = 'autotest'

# Read arguments
usage = '%prog <shelfId>'
parser = optparse.OptionParser(usage = usage)
(opts, args) = parser.parse_args()

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

ub = telnet(UBUNTU, UBUNTU_LOGIN, UBUNTU_PASSWORD, '\$')
ub.send_expect('telnet 127.11.' + args[0] + '.122', 'login:')
ub.send_expect(CSIM_LOGIN, 'Password:')
ub.send_expect(CSIM_PASSWD, '#')

ub.logfile = None
ub.interact()

