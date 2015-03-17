from telnet import telnet
from ftp import ftp
import os
import optparse
import sys

IP = '10.220.16.181'
LOGIN = 'guest'
PASSWORD = 'guest'
CPU = os.getenv('C_CPU')

# Read arguments
ARG_COUNT = 1
usage = '%prog <build> [options]'
parser = optparse.OptionParser(usage = usage)
parser.add_option('-i', '--ip', dest='ip', help='NE IP Address')
parser.add_option('-l', '--login', dest='login', help='Ip address of target')
parser.add_option('-p', '--password', dest='password', help='Ip address of target')
(opts, args) = parser.parse_args()

if opts.ip:
    IP = opts.ip

if opts.login:
    LOGIN = opts.login

if opts.password:
    PASSWORD = opts.password

if len(args) != ARG_COUNT:
    parser.print_usage()
    sys.exit(0)

tel = telnet(IP, 'root', 'infinera', '#')
tel.run('cd /f0/base/tar')
tel.send_expect('ftp 10.220.0.66', 'Name')
tel.send_expect('nsujir', 'Password')
tel.send_expect('f', 'ftp>')
tel.send_expect('cd dawn_v1/xtndev/tar_ne', 'ftp>')
tel.send_expect('bin', 'ftp>')
tel.send_expect('get ' + args[0] + '.' + CPU + '.tar.gz', 'ftp>')

sys.exit(0)

ft = ftp(IP, LOGIN, PASSWORD)
ft.run('cd /f0/base/tar')
ft.run('lcd ../tar_ne')
ft.run('tick')
ft.run('put ' + args[0] + '.' + CPU + '.tar.gz')
