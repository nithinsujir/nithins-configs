import pexpect
import optparse
import os
import re
import time
import sys
import shutil
import emailer

#TARGET_IP = '10.220.16.78'
TARGET_IP = '10.220.16.172'
#REBOOT_WAIT = 400
REBOOT_WAIT = 70
R4_VER = 'R4.0.2.0304'
UP_VER = 'R5.1.0.0184'
#UP_VER = 'M6.0.0.3620'
UPGRADE_WAIT = 400
UPGRADE_RETRIES = 20
DOWNGRADE_WAIT = UPGRADE_WAIT
#DOWNGRADE_RETRIES = 20
CARD_AID = '1-a-2'

def spawn_telnet():
    child = pexpect.spawn('telnet ' + TARGET_IP, timeout = UPGRADE_WAIT/UPGRADE_RETRIES)
    child.logfile_read = sys.stdout
    child.logfile = sys.stdout
    child.expect('login:')
    child.sendline('root')
    child.expect('Password:')
    child.sendline('infinera')

    return child

def spawn_tl1():
    for i in xrange(UPGRADE_RETRIES):
        try:
            child = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
            child.logfile_read = sys.stdout
            child.logfile = sys.stdout
            child.expect('TL1>>')
            break

        except pexpect.TIMEOUT:
            print '%2d: Timeout waiting for TL1 prompt. Retrying...' % i
    else:
        raise Exception('Could not connect to TL1 at %s' % TARGET_IP)


    child.sendline('act-user::secadmin:c::infinera1;')
    child.expect('TL1>>')

    return child

def countdown(line, wait_time):
    print '\n'
    for i in range(wait_time):
        print '%s: %2d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%20s\n' % ' '

def delete_db(tl1):
    print 'Retrieving DBs'
    tl1.sendline(r';')
    tl1.expect('TL1>>')
    tl1.send(r'rtrv-rfile:::c;')
    lines = tl1.before + tl1.after
    tl1.expect('COMPLD')
    lines = lines + tl1.before + tl1.after
    tl1.expect('TL1>>')
    lines = lines + tl1.before + tl1.after

    #print '\n\n\n Lines: '
    #print lines

    regx_ver = re.compile('FILE=(.*),FILETYPE=DB')
    for version in regx_ver.findall(lines):
        print 'Deleting db ' + version
        tl1.sendline('dlt-rfile:::ea:::file="file:///' + version + '", type=db;')
        tl1.expect('TL1>>')

def upgrade(tl1):
    delete_db(tl1)
    print 'Upgrading to ' + UP_VER

    for i in xrange(UPGRADE_RETRIES):
        tl1.send(r'apply:::c:::filename="file:///' + UP_VER + '",opertype=upgrade;')
        rval = tl1.expect(['COMPLD', 'operation is in progress'])

        if rval == 0:
            break
    else:
        raise Exception('apply command failed during upgrade')

    countdown('Rebooting', UPGRADE_WAIT)


def downgrade(tl1):
    delete_db(tl1)
    print 'Downgrading to ' + R4_VER
    rval = 0

    for i in xrange(10):
        tl1.send(r'apply:::c:::filename="file:///' + R4_VER + '",opertype=install;')
        rval = tl1.expect(['COMPLD', 'is the Current Software', 'operation is in progress'])

        if rval == 2:
            print '%2d: Upgrade operation still in progress. Retrying...' % i
            time.sleep(10)
            continue
        else:
            break

    if rval == 0:
        countdown('Rebooting', DOWNGRADE_WAIT)
        reset_passwd()
    else:
        print 'Current software is 4.x. Not rebooting'


def check_sapend(tl1):
    tl1.send(r'rtrv-condet-eqpt::' + CARD_AID + ':c;')
    lines = tl1.before + tl1.after
    tl1.expect('COMPLD')
    lines = lines + tl1.before + tl1.after
    tl1.expect('TL1>>')
    lines = lines + tl1.before + tl1.after

    tl1.send(r'rtrv-condet-eqpt::' + CARD_AID + ':c;')
    lines = lines + tl1.before + tl1.after
    tl1.expect('COMPLD')
    lines = lines + tl1.before + tl1.after
    tl1.expect('TL1>>')
    lines = lines + tl1.before + tl1.after

    #print lines
    if 'FIRMWARE-SAPEND' not in lines:
        tel = spawn_telnet()
        tel.expect('#')
        tel.sendline('/sbin/slay tcpdump')
        tel.expect('#')
        tel.sendline('sloginfo > /f0/slog_sapend.txt')
        tel.expect('#')

        em = emailer.Emailer('nsujir@infinera.com', 'nsujir@infinera.com')
        em.send_email('SAPEND Test', 'SAPEND does not exist')

        raise Exception('SAPEND does not exist')


def reset_passwd():
    for i in xrange(UPGRADE_RETRIES):
        try:
            tl1 = pexpect.spawn('telnet ' + TARGET_IP + ' 9090', timeout = UPGRADE_WAIT/UPGRADE_RETRIES)
            tl1.logfile_read = sys.stdout
            tl1.logfile = sys.stdout
            tl1.expect('TL1>>')
            break
        except pexpect.TIMEOUT:
            print '%2d: Timeout waiting for TL1 prompt. Retrying...' % i
    else:
        raise Exception('Could not connect to TL1 at %s' % TARGET_IP)


    tl1.sendline('act-user::secadmin:c::Infinera1;')
    tl1.expect('COMPLD')
    tl1.sendline('ed-pid::secadmin:c::Infinera1,infinera1;')
    tl1.expect('COMPLD')
    tl1.sendline('ed-user-secu::secadmin:c::,,,SA&NA&NE&PR&TT:tmout=0;')
    tl1.expect('COMPLD')
    tl1.sendline('canc-user::secadmin:c;')
    tl1.expect('COMPLD')
    tl1.sendline('act-user::secadmin:c::infinera1;')
    tl1.expect('COMPLD')
    tl1.sendline('alw-dbrepT-ALL:::c;')
    tl1.expect('COMPLD')
    tl1.sendline('rtrv-audit-seculog:::c1:::logevent=commands;')
    tl1.expect('COMPLD')

iter = 0
tl1 = spawn_tl1()

while True:
    print '----[ %d ]--------------------------' % iter

    downgrade(tl1)

    tl1 = spawn_tl1()
    upgrade(tl1)

    # Spawn tl1 and wait until upgrade completes successfully
    tl1 = spawn_tl1()
    print 'Waiting for Upgrade success message'
    tl1.expect('System Upgraded To ' + UP_VER + ' Successfully', timeout = 200)
    check_sapend(tl1)

    print '\n'
    iter = iter + 1
