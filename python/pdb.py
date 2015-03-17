import pexpect
import os
import sys
import optparse

dirs = [ '../../../../src_ne/mcm',
         '../../../../src_ne/mcm/Log',
         '../../../../src_ne/mcm/moapps', 
         '../../../../src_ne/mcm/moapps/eqpt', 
         '../../../../src_ne/mcm/CMog', 
         '../../../../src_ne/sys/mcm/Cmog', 
         '../../../../src_ne/sys/mcm/Mog', 
         '../../../../src_ne/component/TH', 
         '../../../../src_ne/component/DH', 
         '../../../../src_ne/component/Dm', 
         '../../../../src_ne/component/Ics', 
         '../../../../src_ne/component/Mog',
         '/home/nsujir/dawn_v1/3dParty/Rti/custom/ndds_source/libsrc/ndds/nddslib']

LOGIN ='autotest'
PASSWORD ='autotest'
TARGET_IP = '10.220.6.31'
exename = 'NONE'
PROMPT = '#'

#LOGIN ='root'
#PASSWORD ='infinera1'
#TARGET_IP = '10.220.16.181'

def spawn_telnet():
    child = pexpect.spawn('telnet ' + TARGET_IP)
    child.logfile_read = sys.stdout
    child.expect('login:')
    child.sendline(LOGIN)
    child.expect('Password:')
    child.sendline(PASSWORD)

    return child


parser = optparse.OptionParser()
parser.add_option('-e', '--exe', dest='exe', help='Debug Executable')
parser.add_option('-i', '--ip', dest='ip', help='Ip address of target')
parser.add_option('-l', '--login', dest='login', help='Ip address of target')
parser.add_option('-p', '--password', dest='password', help='Ip address of target')
parser.add_option('-z', '--zid', dest='zid', help='Zhost Id')
parser.add_option('-d', '--pid', dest='pid', help='Pid of process to attach to')
parser.add_option('-t', '--prompt', dest='prompt', help='Command line prompt to expect')

(opts, args) = parser.parse_args()


if opts.exe:
    exename = opts.exe

if opts.ip:
    TARGET_IP = opts.ip

if opts.login:
    LOGIN = opts.login

if opts.password:
    PASSWORD = opts.password

if opts.prompt:
    PROMPT = opts.prompt

tel = spawn_telnet()


# Start pdebug
tel.sendline('ps -e | grep pdebug')
try:
    tel.expect('\?', timeout = 2)
    print 'pdebug already running. Not starting'
except:
    # No pdebug exists. Start
    tel.sendline('pdebug 1')
    print 'Starting pdebug'
    tel.expect(PROMPT)


# Find pid of exe
PS = 'ps -e'
if opts.zid:
    PS = 'zps zhost' + opts.zid

if opts.pid:
    pid = opts.pid
else:
    tel.sendline('ls')
    tel.expect(PROMPT)
    tel.sendline(PS + ' | grep ' + exename)
    tel.expect('\s*(\d+)( \?.*)' + exename)
    print tel.match.groups()
    pid, dummy = tel.match.groups()
    print 'Found pid: ' + str(pid)

#Find the later of exe and exe.gdb
mtime = os.path.getmtime(exename)
#print mtime

try:
    gmtime = os.path.getmtime(exename + '.gdb')
    #print gmtime

    if gmtime >= mtime:
        exename = exename + '.gdb'
except:
    pass


print 'Debugging ' + exename


CPU = os.getenv('C_CPU')

gdb = pexpect.spawn('nto' + CPU + '-gdb ' + exename)
gdb.logfile_read = sys.stdout

gdb.expect('gdb')
gdb.sendline('target qnx ' + TARGET_IP + ':1')
gdb.expect('gdb')

for d in dirs:
    gdb.sendline('directory ' + d)
    gdb.expect('gdb')

INF_WRK_AREA_FWD = os.getenv('INF_WRK_AREA_FWD')
INF_3DL = os.getenv('INF_3DL')

CMN_LIB = INF_WRK_AREA_FWD + '/pf_ne/' + CPU + '/cmn/lib'
MCM_LIB = INF_WRK_AREA_FWD + '/pf_ne/' + CPU + '/mcm/lib'
LIB_3D  = INF_WRK_AREA_FWD + '/3d/' + CPU + '/' + INF_3DL

gdb.sendline('set solib-search-path ' + CMN_LIB + ':' + MCM_LIB + ':' + LIB_3D)
gdb.expect('gdb')

gdb.sendline('attach ' + pid)
gdb.expect('gdb')

gdb.interact()
