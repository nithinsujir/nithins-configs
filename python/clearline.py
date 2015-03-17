from expect import expect
import optparse
import sys


# Constants
ARG_COUNT = 2
LOGIN1 = 'Secret'
LOGIN2 = 'secret'

# Read arguments
usage = '%prog <serial server ip> <line>'
parser = optparse.OptionParser(usage = usage)
(opts, args) = parser.parse_args()

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

ser = expect('telnet ' + args[0])
ser.expect('Password:')
ser.sendline(LOGIN1)
ser.expect('>')
ser.sendline('en')
ser.expect('Password:')
ser.sendline(LOGIN2)
ser.expect('#')

for i in range(0,3):
    ser.sendline('clear line ' + args[1])
    ser.expect('confirm')
    ser.sendline('y')
    ser.expect('#')

