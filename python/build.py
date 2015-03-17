import os
import optparse
import sys

MBIN = os.environ['INF_WRK_AREA'] + '/pf_ne/' + os.environ['C_CPU'] + '/mcm/bin/'
CLIB = os.environ['INF_WRK_AREA'] + '/pf_ne/' + os.environ['C_CPU'] + '/cmn/lib/'
MLIB = os.environ['INF_WRK_AREA'] + '/pf_ne/' + os.environ['C_CPU'] + '/mcm/lib/'
HOME = os.environ['HOME']

C_CPU = os.environ['C_CPU']
MAKEOPTS = ''

def make_binary(name):
    print 'Adding ' + name
    command = ' && make -C sys/mcm/' + name + MAKEOPTS
    command = command + ' && mv ' + MBIN + name + ' ' + MBIN + name + '.gdb'
    command = command + ' && nto' + C_CPU + '-strip ' + MBIN + name + '.gdb -o ' + MBIN + name
    command = command + ' && touch ' + MBIN + name + '.gdb'

    return command

def make_mcmd():
    print 'Adding Mcmd'
    command = ' && make -C sys/mcm/' + C_CPU + MAKEOPTS
    command = command + ' && mv ' + MBIN + 'Mcmd' + ' ' + MBIN + 'Mcmd' + '.gdb'
    command = command + ' && nto' + C_CPU + '-strip ' + MBIN + 'Mcmd' + '.gdb -o ' + MBIN + 'Mcmd'
    command = command + ' && touch ' + MBIN + 'Mcmd' + '.gdb'

    return command

def copy_binary(name):
    print 'Copying ' + name
    command = ' && ln -f ' + MBIN + name + ' ' + HOME + '/base/ins/current/bin'
    return command

def make_so():
    print 'Adding libone and libtwo'
    command = ' && make so'

    name = 'libone.so'
    #command = command + ' && cp ' + CLIB + name + ' ' + CLIB + name + '.gdb'
    #command = command + ' && nto' + C_CPU + '-strip ' + CLIB + name

    name = 'libtwo.so'
    #command = command + ' && cp ' + CLIB + name + ' ' + CLIB + name + '.gdb'
    #command = command + ' && nto' + C_CPU + '-strip ' + CLIB + name

    return command

def copy_libone():
    print 'Copying libone and libtwo'

    name = 'libone.so'
    command = ' && ln -f ' + CLIB + name + ' ' + HOME + '/base/ins/current/lib'

    name = 'libtwo.so'
    command = command + ' && ln -f ' + CLIB + name + ' ' + HOME + '/base/ins/current/lib'

    return command

def copy_mlib(libname):
    print 'Copying ' + libname

    command = ' && ln -f ' + MLIB + libname + ' ' + HOME + '/base/ins/current/lib'

    return command
    

parser = optparse.OptionParser()
parser.add_option('-j', '--jobs', dest='jobs')
parser.add_option('', '--eqpt', dest='eqpt', action="store_true")
parser.add_option('', '--smog', dest='smog', action="store_true")
parser.add_option('', '--rosi', dest='rosi', action="store_true")
parser.add_option('', '--mcmd', dest='mcmd', action="store_true")
parser.add_option('', '--ctpl', dest='ctpl', action="store_true")
parser.add_option('', '--sysi', dest='sysi', action="store_true")
parser.add_option('', '--xma', dest='xma', action="store_true")
parser.add_option('', '--cmog', dest='cmog', action="store_true")
parser.add_option('', '--sysc', dest='sysc', action="store_true")
parser.add_option('', '--cog', dest='cog', action="store_true")
parser.add_option('', '--cdm', dest='cdm', action="store_true")
parser.add_option('', '--scmog', dest='scmog', action="store_true")
parser.add_option('', '--mcmog', dest='mcmog', action="store_true")
parser.add_option('', '--mpm', dest='mpm', action="store_true")
parser.add_option('', '--dh',    dest='dh', action="store_true")
parser.add_option('', '--eh',    dest='eh', action="store_true")
parser.add_option('', '--th',    dest='th', action="store_true")
parser.add_option('', '--obmo',    dest='obmo', action="store_true")
parser.add_option('', '--so',  dest='so', action="store_true")
parser.add_option('', '--moapps', dest='moapps', action="store_true")
parser.add_option('', '--tp', dest='tp', action="store_true")
parser.add_option('', '--nob', dest='nob', action="store_true")
parser.add_option('', '--copy', dest='copy', action="store_true")

(opts, args) = parser.parse_args()

command = 'true'

#if opts.nob:
    #MAKEOPTS = MAKEOPTS + ' nob=1'

if opts.jobs:
    MAKEOPTS = MAKEOPTS + ' -j ' + opts.jobs


def build_cmd(dir):
    print 'New cmd'

    command = ''
    if not opts.nob:
        command = ' && make -C ' + dir + ' recurse_ob'
    command = command + ' && make -C ' + dir + ' objs -j 12'
    command = command + ' && make -C ' + dir + ' nob=1 '
    command = command + ' && make -C ' + dir + ' so'

    return command

if opts.obmo:
    command = command + build_cmd('component/ObMo')

if opts.eh:
    command = command + build_cmd('component/EH')

if opts.dh:
    command = command + build_cmd('component/DH')

if opts.th:
    command = command + build_cmd('component/TH')

if opts.cog:
    command = command + build_cmd('component/Og')

if opts.cdm:
    command = command + build_cmd('component/Dm')

if opts.sysc:
    command = command + build_cmd('component/SysCommon')

if opts.cmog:
    command = command + build_cmd('component/Mog')

if opts.eqpt:
    command = command + build_cmd('mcm/moapps/eqpt')

if opts.tp:
    command = command + build_cmd('mcm/TP')

    if opts.copy:
        command = command + copy_mlib('libTP.so') + copy_mlib('libTPob.so')

if opts.moapps:
    command = command + build_cmd('mcm/moapps')

    if opts.copy:
        command = command + copy_mlib('libmoapps.so') + copy_mlib('libmoappsEq.so') + copy_mlib('libmoappsEqob.so')

if opts.mcmog:
    command = command + build_cmd('mcm/CMog')

if opts.mpm:
    command = command + build_cmd('mcm/PM')

if opts.so:
    command = command + make_so()

    if opts.copy:
        command = command + copy_libone()

if opts.smog:
    command = command + make_binary('Mog')

    if opts.copy:
        command = command + copy_binary('Mog')

if opts.ctpl:
    command = command + make_binary('ControlPlane')

    if opts.copy:
        command = command + copy_binary('ControlPlane')

if opts.sysi:
    command = command + make_binary('SysInit')

    if opts.copy:
        command = command + copy_binary('SysInit')

if opts.xma:
    command = command + make_binary('XmaAgent')

    if opts.copy:
        command = command + copy_binary('XmaAgent')

if opts.scmog:
    command = command + make_binary('Cmog')

    if opts.copy:
        command = command + copy_binary('Cmog')

if opts.rosi:
    command = command + make_binary('RoSi')

    if opts.copy:
        command = command + copy_binary('RoSi')

if opts.mcmd:
    command = command + make_mcmd()

    if opts.copy:
        command = command + copy_binary('Mcmd')

print command
rval = os.system(command)

if rval != 0:
    rval = 1

sys.exit(rval)



