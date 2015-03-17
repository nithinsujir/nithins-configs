from telnet import telnet
import optparse
import sys

# Constants
ARG_COUNT = 1
NE = '10.220.16.181'
NE_LOGIN = 'root'
NE_PASSWORD = 'infinera1'

# Read arguments
usage = '%prog <procname>'
parser = optparse.OptionParser(usage = usage)
(opts, args) = parser.parse_args()

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

ne = telnet(NE, NE_LOGIN, NE_PASSWORD, '#')
ne.sendline('ps -e | grep ' + args[0])
ne.expect('\s*(\d+) \?.*' + args[0])
pid = ne.match.groups()

print 'Dumping pid: ' + pid

ne.run('dumper -d /var/dumps -p ' + pid)


FTP_LOGIN = 'guest'
FTP_PASSWD = 'guest'
COREPATH = '/home/nsujir/cores'
ft = ftp(NE, FTP_LOGIN, FTP_PASSWD)
ft.run('lcd /var/dumps')
ft.run('cd ' + COREPATH)
ft.run('get ' + args[0] + '.core')




