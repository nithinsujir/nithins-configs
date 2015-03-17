import pexpect
import sys
import time


COGTYPE = 'CogOrm'
CHASSIS = 1
CARD = 3
FAULT_TEMPLATE = r' <NV N=\"%s-%d-%d\"> <S N=\"FimType\">Cond</S> <NV N=\"FimData\"> <H N=\"0\">%016x</H> <H N=\"1\">0000000000000000</H> <H N=\"2\">0000000000000000</H> <H N=\"3\">0</H> <H N=\"4\">0</H> <H N=\"5\"></H> <H N=\"6\">0000000000000000</H> <H N=\"7\"></H> <H N=\"8\"></H> </NV> </NV> ' 
#FAULT_TEMPLATE = r' <NV N=\"%s-%d-%d\"> <S N=\"FimType\">Cond</S> <NV N=\"FimData\"> <H N=\"0\">%016x</H> <H N=\"1\">0000000000000000</H> <H N=\"2\">0000000000000000</H> <H N=\"3\">00000000000000000000000000000000</H> <H N=\"4\">0000000000000000</H> <H N=\"5\"></H> <H N=\"6\">0000000000000000</H> <H N=\"7\"></H> <H N=\"8\"></H> </NV> </NV> ' 

#COGTYPE = 'DlmCog'
#CHASSIS = 1
#CARD = 3
#FAULT_TEMPLATE = r' <NV N=\"%s-%d-%d\"> <S N=\"FimType\">Cond</S> <NV N=\"FimData\"> <H N=\"0\">0</H> <H N=\"1\"></H> <H N=\"2\"></H> <H N=\"3\"></H> <H N=\"4\"></H> <H N=\"5\"></H> <H N=\"6\">0000000000000000</H> <H N=\"7\">0103002004050607</H> <H N=\"8\">%012x</H> </NV> </NV> '

TARGET_IP = '10.220.6.31'
LOGIN ='autotest'
PASSWORD ='autotest'

def spawn_telnet():
    child = pexpect.spawn('telnet ' + TARGET_IP)
    #child.logfile_read = sys.stdout
    child.expect('login:')
    child.sendline(LOGIN)
    child.expect('Password:')
    child.sendline(PASSWORD)

    return child

def spawn_tl1():
    child = pexpect.spawn('telnet ' + TARGET_IP + ' 9090')
    child.logfile_read = sys.stdout
    child.expect('TL1>>')
    child.sendline('act-user::secadmin:c::infinera1;')
    child.expect('Your password')

    return child


# Create /tmp/fault.xml with the fault template and run it
def set_fault(tel, fault):
    fault_string = FAULT_TEMPLATE % (COGTYPE, CHASSIS, CARD, fault)

    tel.sendline(r'echo "' + fault_string + r'" > /tmp/fault.xml')
    tel.expect(r'$')
    tel.sendline(r'$insx/bin/IcsSpy -p /Fm/%s-%d-%d /tmp/fault.xml' % (COGTYPE, CHASSIS, CARD))
    tel.expect(r'Exiting..')
    

def rtrv_cond(tl1):
    tl1.send('rtrv-condet-eqpt::%d-A-%d:c;' % (CHASSIS, CARD))
    tl1.expect('COMPLD')
    #print tl1.before + tl1.after
    tl1.send('rtrv-cond-all::%d-A-%d:c;' % (CHASSIS, CARD))
    tl1.expect('COMPLD')
    #print tl1.before + tl1.after

tl1 = spawn_tl1()
tel = spawn_telnet()

set_fault(tel, 2**2)
time.sleep(3)
rtrv_cond(tl1)
sys.exit(0)

for i in range(30):
    print '\n\n============================== Bit %d =========================' % i

    set_fault(tel, 2**i)
    time.sleep(3)
    rtrv_cond(tl1)
    time.sleep(2)
