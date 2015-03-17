import ftplib
import pexpect
import optparse
import os
import re
import time
import sys

parser = optparse.OptionParser()
parser.add_option('-v', '--version', dest='version', help='Install Version')
(opts, args) = parser.parse_args()

if not opts.version:
    parser.error('Need version to install')


TARGET_IP = '10.220.6.31'
LOGIN ='autotest'
PASSWORD ='autotest'
FTP_WAIT = 60

def spawn_ftp():
    print 'Logging into ftp...'
    ftp = pexpect.spawn('ftp ' + TARGET_IP, logfile = sys.stdout)
    #ftp.logfile_read = sys.stdout
    ftp.expect('Name')
    ftp.sendline(LOGIN)
    ftp.expect('Password:')
    ftp.sendline(PASSWORD)

    ftp.expect('ftp>')

    ftp.sendline('bin')

    ftp.expect('ftp>')

    return ftp


def upload_tar(ftp, version):
    ftp.sendline('lcd ../tar_ne')
    ftp.expect('ftp>')

    ftp.sendline('put ' + version + '.x86.tar.gz')
    ftp.expect('ftp>', timeout = FTP_WAIT)

    ftp.sendline('by')


def spawn_telnet():
    child = pexpect.spawn('telnet ' + TARGET_IP)
    child.logfile_read = sys.stdout
    child.expect('login:')
    child.sendline(LOGIN)
    child.expect('Password:')
    child.sendline(PASSWORD)

    return child

#ftpobj = spawn_ftp()
#upload_tar(ftpobj, opts.version)

telobj = spawn_telnet()
telobj.sendline('touch ' + opts.version + '.x86.tar.gz')
telobj.expect('\$')
#telobj.sendline('sa')
#telobj.expect('\$')
telobj.sendline('zloadimage ' + opts.version + ' zhost1 zhost2 zhost3 zhost4')
telobj.expect('\$')
telobj.sendline('zinstallimage ' + opts.version + ' zhost1 zhost2 zhost3 zhost4')
telobj.expect('Successfully installed image')

