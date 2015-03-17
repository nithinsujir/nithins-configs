#!/usr/bin/env python
import pexpect
import sys
import time

CRASH_WAIT = 550
VMCORE_WAIT = 1250
SSH_RETRIES = 20

def countdown(line, wait_time):
    for i in range(wait_time):
        print '%s: %3d...\r' % (line, (wait_time - i)),
        sys.stdout.flush()
        time.sleep(1)
    print '%80s\r' % ' '

def send_expect(handle, send_line, expect_line, timeout):
    start = time.time()

    print 'Waiting upto %d seconds for vmcore.gz' % timeout

    while True:
        try:
            handle.sendline(send_line)
            handle.expect(expect_line)
            break
        except:
            if (time.time() - start) < timeout:
                pass
                time.sleep(30)
                print 'Waiting upto %d seconds for vmcore.gz' % (timeout - (time.time() - start))
            else:
                raise BaseException('Timeout waiting for', expect_line, 'after ', send_line)

if len(sys.argv) < 2:
	sys.exit(sys.argv[0] + ' <server> [password]')

server = sys.argv[1]

password = 'tintri99'
if len(sys.argv) > 2:
	password = sys.argv[2]

i = 0
retried = 0
while True:
    print 'Iteration: %d' % i

    try:
        ssh = pexpect.spawn('ssh ' + server + ' -l root')
        ssh.logfile = sys.stdout

        rc = ssh.expect(['#', '\$', 'password:', 'RSA key fingerprint'], timeout = 120)

        if rc == 0 or rc == 1:
            pass
        else:
            if rc == 3:
                ssh.sendline('yes')
                ssh.expect(['Password:', 'password:'])

            ssh.sendline(password)
            ssh.expect(['#', '\$'])
    except:
        if retried < SSH_RETRIES:
            pass
            retried = retried + 1
            time.sleep(1)
            continue

    retried = 0
    ssh.sendline('ls -l /var/corefiles/kernel*')

    if i > 0:
        try:
            ssh.expect('vmcore.gz')
        except:
            send_expect(ssh, 'ls -l /var/corefiles/kernel*', 'vmcore.gz', VMCORE_WAIT)

    ssh.sendline('echo 900 > /sys/module/ipmi_watchdog/parameters/timeout')
    ssh.expect('#')
    ssh.sendline('cat /sys/module/ipmi_watchdog/parameters/timeout')
    ssh.expect('900')
    #ssh.sendline('ipmitool mc watchdog off')
    #ssh.expect('stopped')
    #ssh.sendline('ipmitool bmc watchdog off')
    #ssh.expect('stopped')
    ssh.sendline('pkill -9 savecore')
    ssh.expect('#')
    ssh.sendline('pkill -9 gzip')
    ssh.expect('#')
    time.sleep(2)
    ssh.sendline('pkill -9 gzip')
    ssh.expect('#')
    ssh.sendline('rm -rf /var/corefiles/kernel*')
    ssh.expect('#')
    ssh.sendline('sync')
    ssh.expect('#')

    # Config dump
    #ssh.sendline('rmmod diskdump')
    #ssh.expect('#')
    #ssh.sendline('modprobe diskdump')
    #ssh.expect('#')
    #ssh.sendline('/root/config_dump -c -v')
    #ssh.expect('#')

    # Start dperf
    #ssh.sendline('mount localhost:/tintri /mnt')
    #ssh.expect('#')
    #ssh.sendline('mount')
    #ssh.expect('tintri')
    #ssh.sendline('rm -f /var/corefiles/out')
    #ssh.expect('#')
    #ssh.sendline('touch /var/corefiles/out')
    #ssh.expect('#')
    #ssh.sendline('dperf --range 1g --work w-16k-16 /var/corefiles/out &')
    #ssh.sendline('')
    #ssh.expect('#')

    countdown('Crashing system in', 10)
    ssh.sendline('top -b -n 1 | head -n 15')
    ssh.expect('#')
    ssh.sendline('ls -l /var/corefiles/*')
    ssh.expect(['No such file', 'total 0'])

    ssh.sendline('echo c > /proc/sysrq-trigger')

    countdown('Waiting for crashdump', CRASH_WAIT)
    i = i + 1

