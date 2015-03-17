#!/usr/bin/env python
from telnet import telnet
import optparse
import re

IP = '10.220.16.181'
LOGIN = 'root'
PASSWORD = 'infinera1'
DBIPROMPT = 'dbi->'

parser = optparse.OptionParser()
parser.add_option('-i', '--ip', dest='ip', help='NE IP Address')
parser.add_option('-l', '--login', dest='login', help='Ip address of target')
parser.add_option('-p', '--password', dest='password', help='Ip address of target')
(opts, args) = parser.parse_args()

if opts.ip:
    IP = opts.ip
    if not re.match('\d+\.\d+\.\d+\.\d+', IP):
        IP = '10.220.16.' + opts.ip


if opts.login:
    LOGIN = opts.login

if opts.password:
    PASSWORD = opts.password


ub = telnet(IP, LOGIN, PASSWORD, '#')
ub.send_expect('dbiClient -n', DBIPROMPT)
ub.send_expect('@sd 0', DBIPROMPT)
ub.send_expect('@ss CpDbi', DBIPROMPT)
ub.send_expect('bcm stg stp 1 fe11 forward', DBIPROMPT)

