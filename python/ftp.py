#!/usr/bin/python
# Script to ftp files to x86/ppc
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


import pexpect
import optparse
import os
import re
import time
import sys
from library.ftp import ftp as Ftp
from library.telnet import telnet as Telnet

TARGET_IP = '10.220.6.31'
#TARGET_IP = '10.220.6.36'
REBOOT_WAIT = 60
TARUN_WAIT = 250
DB_WAIT = 90
FTP_WAIT = 900
CPU ='x86'
LOGIN ='autotest'
PASSWORD ='autotest'
#PASSWORD ='a'
FTP_TMP = '/f0'
TELNET_PROMPT = '\$'

def get_base_dir():
    parent, current = os.path.split(os.getcwd())
    print 'Starting in %s %s' % (parent, current)

    while current != 'main' and current != 'fuji' and current != 'ganga' and current != 'xtndev' and parent != '/':
        parent, current = os.path.split(parent)
        print 'Processing %s %s' % (parent, current)

    if parent == '/':
        print '*** Error: ftp has to be run in the source tree'
        sys.exit(-1)
        

    dirname = os.path.join(parent, current)
    #dirname = os.path.join(dirname, 'main')

    return dirname



base_dir = get_base_dir()
print 'Base dir is ' + base_dir


class error():
    def __init__ (self, err_string):
        self.err_string = err_string

def spawn_ftp():
    print 'Logging into ftp...'
    return Ftp(TARGET_IP, LOGIN, PASSWORD)

def upload_file(ftp, name):
    src_path, dst_path = paths[name]
    #ftp.expect('ftp>')

    print 'Sending file ' + src_path
    ftp.run('!ls -l ' + src_path)
    ftp.run('put ' + src_path + ' ' + FTP_TMP + '/' + name, FTP_WAIT)

    print 'Done'

def close_ftp(ftp):
    try:
        ftp.run('by')
    except pexpect.EOF:
        # We get a EOF here because expect for prompt fails after bye
        pass


def spawn_telnet():
    return Telnet(TARGET_IP, LOGIN, PASSWORD, TELNET_PROMPT)



def move_file(telnet_obj, name, make_exec = False):
    src_path, dst_path = paths[name]

    telnet_obj.run('mv $INS_ROOT/' + dst_path + '/' + name + ' $INS_ROOT/' + dst_path + '/' + name + '.orig')
    telnet_obj.run('mv ' + FTP_TMP + '/' + name + ' $INS_ROOT/' + dst_path)

    if make_exec:
        print '\nMaking ' + os.path.join(dst_path, name) + ' executable'
        telnet_obj.run('/bin/chmod +x $INS_ROOT/' + os.path.join(dst_path, name))




#==================================== START MAIN ======================================================

# Parse command line options
parser = optparse.OptionParser()
parser.add_option('-c', '--ctpl', dest='ctpl', action="store_true", help='Install ControlPlane')
parser.add_option('-d', '--rdb', dest='rdb', action="store_true", help='Install RdbSvr')
parser.add_option('-f', '--fim', dest='fim', action="store_true", help='Install Fim')
parser.add_option('-g', '--grdb', dest='grdb', action="store_true", help='Install GrdbSvr')
parser.add_option('-i', '--ip', dest='ip', help='Ip address')
parser.add_option('-l', '--libone', dest='libone', action="store_true", help='Install libone.so')
parser.add_option('', '--ltp', dest='libtp', action="store_true", help='Install libtp')
parser.add_option('', '--lmo', dest='libmoapps', action="store_true", help='Install libmoapps')
parser.add_option('-m', '--mog', dest='mog', action="store_true", help='Install Mog')
parser.add_option('', '--sysi', dest='sysi', action="store_true", help='Install SysInit')
parser.add_option('-x', '--xma', dest='xma', action="store_true", help='Install XmaAgent')
parser.add_option('-n', '--mcmd', dest='mcmd', action="store_true", help='Install Mcmd')
parser.add_option('-o', '--cmog', dest='cmog', action="store_true", help='Install Cmog')
parser.add_option('-r', '--rosi', dest='rosi', action="store_true", help='Install RoSi')
parser.add_option('-s', '--test', dest='test', action="store_true", help='Install test')
parser.add_option('-t', '--tl1', dest='tl1', action="store_true", help='Install Tl1Agent')
parser.add_option('-w', '--web', dest='web', action="store_true", help='Install WebServer')
(opts, args) = parser.parse_args()

# If ip is given, assume ppc
if opts.ip:
    CPU = 'ppc'
    LOGIN = 'guest'
    PASSWORD = 'guest'

    TARGET_IP = opts.ip
    if not re.match('\d+\.\d+\.\d+\.\d+', TARGET_IP):
        TARGET_IP = '10.220.16.' + opts.ip

    TELNET_PROMPT = '#'

MCM_BIN_PATH = 'pf_ne/' + CPU + '/mcm/bin'
CMN_LIB_PATH = 'pf_ne/' + CPU + '/cmn/lib'
MCM_LIB_PATH = 'pf_ne/' + CPU + '/mcm/lib'

paths = {}
paths['Mog'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'Mog')), 'bin')
paths['SysInit'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'SysInit')), 'bin')
paths['XmaAgent'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'XmaAgent')), 'bin')
paths['Cmog'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'Cmog')), 'bin')
paths['GRdbSvr'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'GRdbSvr')), 'bin')
paths['RdbSvr'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'RdbSvr')), 'bin')
paths['ControlPlane'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'ControlPlane')), 'bin')
paths['Mcmd'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'Mcmd')), 'bin')
paths['Fim'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'Fim')), 'bin')
paths['RoSi'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'RoSi')), 'bin')
paths['test'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'test')), 'bin')
paths['RdbSvr'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'RdbSvr')), 'bin')
paths['Tl1Agent'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'Tl1Agent')), 'bin')
paths['WebServer'] = (os.path.join(base_dir, os.path.join(MCM_BIN_PATH, 'WebServer')), 'bin')
paths['libone.so'] = (os.path.join(base_dir, os.path.join(CMN_LIB_PATH, 'libone.so')), 'lib')
paths['libtwo.so'] = (os.path.join(base_dir, os.path.join(CMN_LIB_PATH, 'libtwo.so')), 'lib')
paths['libTP.so'] = (os.path.join(base_dir, os.path.join(MCM_LIB_PATH, 'libTP.so')), 'lib')
paths['libTPob.so'] = (os.path.join(base_dir, os.path.join(MCM_LIB_PATH, 'libTPob.so')), 'lib')
paths['libmoapps.so'] = (os.path.join(base_dir, os.path.join(MCM_LIB_PATH, 'libmoapps.so')), 'lib')
paths['libmoappsEq.so'] = (os.path.join(base_dir, os.path.join(MCM_LIB_PATH, 'libmoappsEq.so')), 'lib')
paths['libmoappsEqob.so'] = (os.path.join(base_dir, os.path.join(MCM_LIB_PATH, 'libmoappsEqob.so')), 'lib')

telobj = spawn_telnet()
ftpobj = spawn_ftp()
ftpobj.run('tick')

if opts.mog:
    upload_file(ftpobj, 'Mog')
    move_file(telobj, 'Mog', make_exec = True)

if opts.sysi:
    upload_file(ftpobj, 'SysInit')
    move_file(telobj, 'SysInit', make_exec = True)

if opts.xma:
    upload_file(ftpobj, 'XmaAgent')
    move_file(telobj, 'XmaAgent', make_exec = True)

if opts.cmog:
    upload_file(ftpobj, 'Cmog')
    move_file(telobj, 'Cmog', make_exec = True)

if opts.ctpl:
    upload_file(ftpobj, 'ControlPlane')
    move_file(telobj, 'ControlPlane', make_exec = True)

if opts.rdb:
    upload_file(ftpobj, 'RdbSvr')
    move_file(telobj, 'RdbSvr', make_exec = True)

if opts.mcmd:
    upload_file(ftpobj, 'Mcmd')
    move_file(telobj, 'Mcmd', make_exec = True)

if opts.fim:
    upload_file(ftpobj, 'Fim')
    move_file(telobj, 'Fim', make_exec = True)

if opts.test:
    upload_file(ftpobj, 'test')
    move_file(telobj, 'test', make_exec = True)

if opts.rosi:
    upload_file(ftpobj, 'RoSi')
    move_file(telobj, 'RoSi', make_exec = True)

if opts.tl1:
    upload_file(ftpobj, 'Tl1Agent')
    move_file(telobj, 'Tl1Agent', make_exec = True)

if opts.web:
    upload_file(ftpobj, 'WebServer')
    move_file(telobj, 'WebServer', make_exec = True)

if opts.libone:
    upload_file(ftpobj, 'libone.so')
    move_file(telobj, 'libone.so', make_exec = True)
    upload_file(ftpobj, 'libtwo.so')
    move_file(telobj, 'libtwo.so', make_exec = True)

if opts.libtp:
    upload_file(ftpobj, 'libTP.so')
    move_file(telobj, 'libTP.so', make_exec = True)

    upload_file(ftpobj, 'libTPob.so')
    move_file(telobj, 'libTPob.so', make_exec = True)


if opts.libmoapps:
    upload_file(ftpobj, 'libmoapps.so')
    move_file(telobj, 'libmoapps.so', make_exec = True)

    upload_file(ftpobj, 'libmoappsEq.so')
    move_file(telobj, 'libmoappsEq.so', make_exec = True)

    upload_file(ftpobj, 'libmoappsEqob.so')
    move_file(telobj, 'libmoappsEqob.so', make_exec = True)


close_ftp(ftpobj)
#telobj.close()


