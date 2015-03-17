from telnet import telnet
import optparse
import sys

# Constants
ARG_COUNT = 2
NE = '10.220.16.181'
NE_LOGIN = 'root'
NE_PASSWORD = 'infinera1'

# Read arguments
usage = '%prog <neip> <shelfId>'
parser = optparse.OptionParser(usage = usage)
(opts, args) = parser.parse_args()

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

ub = telnet(NE, NE_LOGIN, NE_PASSWORD, '#')
ub.send_expect('telnet 127.1.' + args[1] + '.122', 'login:')
ub.send_expect('root', '#')

ub.logfile = None
ub.interact()


