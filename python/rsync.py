import os

HOME = '/home/nsujir'
BLD_SVR = HOME + '/bld-nsujir'
DEPOT = '/Depot'
XTN_GIT = '/dawn_v1/xtndev/src_ne/.git'

dirs = {
    BLD_SVR + DEPOT : HOME + DEPOT,
    BLD_SVR + XTN_GIT : HOME + '/gitbackups' + XTN_GIT,
    BLD_SVR + '/bin' : HOME + '/bin'
}

for d in dirs.keys():
    print 'Syncing ' + d + ' to ' + dirs[d]
    os.system('mkdir -p ' + os.path.dirname(dirs[d]))
    os.system('rsync -rvt ' + d + ' ' + os.path.dirname(dirs[d]))


