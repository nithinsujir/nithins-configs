#!/usr/bin/python
# Script to telnet to x86/ppc
# Author: nsujir
# 
# Requires cygwin. Install inetutils and python packages
# 
# Download pexpect source and install it from cygwin
#
#   wget http://pexpect.sourceforge.net/pexpect-2.3.tar.gz
#   tar xzf pexpect-2.3.tar.gz
#   cd pexpect-2.3
#   python ./setup.py install

# Usage: if -t option is given, script will install the tar file
# If no option, it will telnet to the x86/ppc


import ftplib
import pexpect
import optparse
import os
import re
import time
import sys
import shutil

TARGET_IP = '10.220.6.31'
REBOOT_WAIT = 60
TARUN_WAIT = 250
APPLY_WAIT = 120
DB_WAIT = 400
DBI_WAIT = 60
FTP_WAIT = 400
GUNZIP_WAIT = 400
CPU = 'x86'
LOGIN ='autotest'
PASSWORD ='autotest'
FTPROOT = '/home/nsujir'
FTPIP = '10.220.0.66'
FTPUSER = 'nsujir'
FTPPASSWD = 'f'
PROMPT = '\$'
TUN_LOGIN = 'a'
TUN_PASSWORD = 'a'

# Parse command line options
parser = optparse.OptionParser()
parser.add_option('-t', '--tgz', dest='tgz', help='tgz to install')
parser.add_option('-p', '--passwd', dest='passwd', action='store_true', help='Reset passwd')
parser.add_option('-e', '--empty_start', dest='emp', action='store_true', help='Restart with empty database')
parser.add_option('-s', '--normal_start', dest='start', action='store_true', help='Normal Start')
parser.add_option('-i', '--ip', dest='ip', help='Ip address')
parser.add_option('-S', '--ssh', action='store_true', dest='ssh', help='Use ssh')
parser.add_option('-l', '--tl1', action='store_true', dest='tl1', help='Start tl1')
parser.add_option('-d', '--dbi', action='store_true', dest='dbi', help='Start dbiClient')
parser.add_option('-z', '--zhost', dest='zhost', help='Connect to zhost')
parser.add_option('-L', '--slog', action='store_true', dest='slog', help='Start sloginfo')
parser.add_option('', '--tun', dest='tunip', help='Start sloginfo')

(opts, args) = parser.parse_args()

# If ip is given, assume ppc
if opts.ip:
    CPU = 'ppc'
    LOGIN = 'guest'
    PASSWORD = 'guest'

    TARGET_IP = opts.ip

    if not re.match('\d+\.\d+\.\d+\.\d+', TARGET_IP):
        TARGET_IP = '10.220.16.' + opts.ip

    print 'Target IP: ' + TARGET_IP
    PROMPT = '#'

if opts.zhost:
    LOGIN = opts.zhost
    PASSWORD = None

class error():
    def __init__ (self, err_string):
        self.err_string = err_string

def upload_file(fil):
    print 'Logging into ftp...'
    ftp = pexpect.spawn('ftp ' + TARGET_IP, logfile = sys.stdout)
    #ftp.logfile_read = sys.stdout
    ftp.expect('Name')
    ftp.sendline(LOGIN)
    ftp.expect('Password:')
    ftp.sendline(PASSWORD)

    ftp.expect('ftp>')

    ftp.sendline('bin')

    name = os.path.split(fil)
    ftp.expect('ftp>')
    ftp.sendline('lcd ' + name[0])

    print 'Local dir now ' + name[0]

    ftp.expect('ftp>')

    print 'Sending file ' + name[1]
    ftp.sendline('put ' + name[1])

    # Wait sometime for transfer
    ftp.expect('ftp>', timeout=FTP_WAIT)
    print 'Done'
    ftp.sendline('by')
    ftp.close()


def spawn_telnet(target_ip = TARGET_IP, login = LOGIN, password = PASSWORD):
    child = pexpect.spawn('telnet ' + target_ip)
    #child.logfile_read = sys.stdout
    child.expect('login:')
    child.sendline(login)

    if PASSWORD != None:
        child.expect('Password:')
        child.sendline(password)

    return child


def reset_passwd():
    print 'Resetting passwd'
    if (opts.tunip):
        tel = spawn_telnet(opts.tunip, TUN_LOGIN, TUN_PASSWORD)
        tel.logfile_read = sys.stdout
        tel.sendline('telnet ' + TARGET_IP + ' 9090')
    else:
        tel = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
    tel.logfile_read = sys.stdout
    tel.expect('TL1>>')

    print 'Sending Infinera1'
    tel.sendline('act-user::secadmin:c::Infinera1;')
    tel.expect('COMPLD')
    tel.sendline('ed-pid::secadmin:c::Infinera1,infinera1;')
    tel.expect('COMPLD')
    tel.sendline('ed-user-secu::secadmin:c::,,,SA&NA&NE&PR&TT:tmout=0;')
    tel.expect('COMPLD')
    tel.sendline('canc-user::secadmin:c;')
    tel.expect('COMPLD')
    tel.sendline('act-user::secadmin:c::infinera1;')
    tel.expect('COMPLD')
    tel.sendline('alw-dbrepT-ALL:::c;')
    tel.expect('COMPLD')
    tel.sendline('rtrv-audit-seculog:::c1:::logevent=commands;')
    tel.expect('COMPLD')

    tel.interact()


def spawn_tl1():
    if (opts.tunip):
        print 'Tunnelling through ' + opts.tunip
        child = spawn_telnet(opts.tunip, TUN_LOGIN, TUN_PASSWORD)
        child.logfile_read = sys.stdout
        child.sendline('telnet ' + TARGET_IP + ' 9090')
    else:
        child = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
        child.logfile_read = sys.stdout

    child.expect('TL1>>')
    child.sendline('act-user::secadmin:c::infinera1;')
    rval = child.expect(['Your password', 'DENY'])

    if rval == 0:
        return child
    else:
        reset_passwd()


def spawn_ssh():
    print 'ssh'
    child = pexpect.spawn('ssh ' + LOGIN + '@' + TARGET_IP, logfile = sys.stdout)
    #child.logfile_read = sys.stdout
    #child.expect('login:')
    #child.sendline('autotest')
    child.expect('password:')
    child.sendline(PASSWORD)

    return child

def get_version(tgz_name):
    name = os.path.split(tgz_name)
    m = re.match('(.*).(x86|ppc).tar.gz', name[1])

    if m:
        return m.group(1)
    else:
        raise error('Cannot parse tgz name')


def countdown(line, wait_time):
    print '\n'
    for i in range(wait_time):
        print '%s: %2d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%40s\n' % ' '


def mcm_install(tgz_name):
    opt_regx = re.compile('(\d+)\) (.\d+.\d+.\d+.\d+)')

    ver = get_version(tgz_name)

    # Connect to the machine
    print 'Logging into telnet'
    child = spawn_telnet()
    child.logfile = sys.stdout

    child.expect(PROMPT)
    child.sendline('mcm_install')

    child.expect('Enter selection:')
    child.sendline('1')

    child.expect('Enter base')
    child.sendline('')

    child.expect('Enter selection:')
    child.sendline('2')

    child.expect('Available choices(.*)Enter selection number:')
    lines = child.match.groups()

    for opt, base in opt_regx.findall(lines[0]):
        if base == ver:
            child.sendline(opt)
            break

    child.expect('Enter selection:')
    child.sendline('3')

    child.expect('Link setup_env', timeout=GUNZIP_WAIT)
    child.sendline('')

    child.expect('Enter selection:')
    child.sendline('11')

    child.expect('Link setup_env')
    child.sendline('')

    child.expect('Enter selection:')
    child.sendline('12')

    child.expect('Enter selection:')
    child.sendline('13')

    child.expect('Enter selection:')
    child.sendline('14')

    child.expect('Enter selection:')
    child.sendline('15')

    child.expect('Enter selection:')
    child.sendline('')

    child.expect('Enter selection:')
    child.sendline('')

    child.expect('Enter selection:')
    child.sendline('q')

    child.expect(PROMPT)
    child.sendline('. .profile')

    child.expect(PROMPT)
    #child.sendline('shutdown')

    # Sleep for reboot
    #countdown('Rebooting...', REBOOT_WAIT)


#==================================== START MAIN ======================================================

# tgz given. Install it
if opts.passwd:
    reset_passwd()
elif opts.tgz:
    # If ip specified, run ppc tl1 install
    if opts.ip:
        child = spawn_tl1()

        if not os.path.exists(os.path.join(FTPROOT, os.path.split(opts.tgz)[1])):
            # Copy the tgz file to ftproot
            print 'Copying ' + opts.tgz + ' to ' + FTPROOT
            shutil.copy(opts.tgz, FTPROOT)
        else:
            print 'Not copying ' + opts.tgz + ' to ' + FTPROOT

        print 'Sending retrieve command'
        child.sendline(r';')
        child.expect('TL1>>')
        child.send(r'rtrv-rfile:::c;')
        lines = child.before + child.after
        child.expect('COMPLD')
        lines = lines + child.before + child.after
        child.send(r';')
        child.expect('TL1>>')
        lines = lines + child.before + child.after


        print '\n\n\n Lines: '
        print lines

        regx_ver = re.compile('SWVERSION=(.*),FORMAT')
        for version in regx_ver.findall(lines):
            print 'Found version ' + version
            child.sendline('dlt-rfile:::ea:::file="file:///' + version + '", type=sw;')
            child.sendline('dlt-rfile:::ea:::file="file:///' + version + '", type=db;')

        child.expect('TL1>>')

        child.sendline(r'copy-rfile:::c:::type=swdl,src="ftp://' + FTPUSER + ':' + FTPPASSWD + '@' + FTPIP + '//' + get_version(opts.tgz) + '.ppc";')
        child.expect('process started')
        child.expect('Copy File Completed', timeout = 300)

        countdown('Waiting for image to be available for install', APPLY_WAIT)
        child.sendline(r'apply:::c:::filename="file:///' + get_version(opts.tgz) + '",opertype=install;')

        child.expect('Install in progress')

        sys.exit(0)


    # else run x86 install
    else:
        upload_file(opts.tgz)
        mcm_install(opts.tgz)

        sys.exit(0)

        child = spawn_telnet()
        child.logfile = sys.stdout
        child.expect(PROMPT)
        child.sendline('taRunSysInit ' + get_version(opts.tgz))

        i = child.expect(['empty database or restore', 'not prepared for this target'], timeout = TARUN_WAIT)
        if i == 0:
            child.sendline('empty')


        child.expect('Ignoring the TELNET security', timeout = DB_WAIT)

        if i==0:
            reset_passwd()

    child.interact()
elif opts.emp:
    child = spawn_telnet()
    child.logfile = sys.stdout
    child.expect(PROMPT)
    child.sendline('tr')
    child.expect('empty database or restore', timeout = TARUN_WAIT)
    child.sendline('empty')
    child.expect('Ignoring the TELNET security', timeout = DB_WAIT)
    reset_passwd()
    child.interact()
elif opts.start:
    child = spawn_telnet()
    child.expect(PROMPT)
    child.sendline('tr')
    child.interact()

elif opts.ssh:
    child = spawn_ssh()
    child.interact()

elif opts.tl1:
    child = spawn_tl1()
    child.interact()

elif opts.dbi:
    child = spawn_telnet()
    child.expect(PROMPT)
    child.sendline('dbiClient -n')
    child.expect('dbi->', timeout = DBI_WAIT)
    child.sendline('@sd 0')
    child.expect('dbi->')
    child.sendline('@ss Mog')
    child.expect('dbi->')
    child.sendline('')
    child.expect('dbi->')
    child.interact()

elif opts.slog:
    child = spawn_telnet()
    child.expect(PROMPT)
    child.sendline('sloginfo -f')
    child.interact()

else:
    child = spawn_telnet()
    child.interact()



