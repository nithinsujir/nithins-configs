import collections
import time
import os
import optparse

class tar_info:
    def __init__(self, name, ctime, client):
        self.name = name
        self.ctime = ctime
        self.client = client


parser = optparse.OptionParser()
parser.add_option('-d', '--del', dest='delete', action='store_true', help='Delete old files')
(opts, args) = parser.parse_args()

ppc_list = collections.defaultdict(list)
x86_list = collections.defaultdict(list)

ppc_list = []
x86_list = []

def add_file(dirname, client, delete):
    fils = os.listdir(dirname)
    fils.sort()
    fils.reverse()
    ppc_added = False
    x86_added = False

    for fil in fils:
        if fil == 'ppc' or fil == 'x86':
            continue

        ctime = time.localtime(os.path.getmtime(os.path.join(dirname, fil)))

        if 'ppc' in fil:
            # If not added add it, if already added, delete all the remaining files
            if not delete or not ppc_added:
                ppc_list.append(tar_info(fil, time.strftime('%b %d, %I:%M %p', ctime), client))
                ppc_added = True
            else:
                ppc_list.append(tar_info(fil, time.strftime('%b %d, %I:%M %p', ctime), 'x'))
                os.remove(os.path.join(dirname, fil))
        else:
            # If not added add it, if already added, delete all the remaining files
            if not delete or not x86_added:
                x86_list.append(tar_info(fil, time.strftime('%b %d, %I:%M %p', ctime), client))
                x86_added = True
            else:
                x86_list.append(tar_info(fil, time.strftime('%b %d, %I:%M %p', ctime), 'x'))
                os.remove(os.path.join(dirname, fil))



add_file(os.getenv('tm1'), '1', opts.delete)
add_file(os.getenv('tm2'), '2', opts.delete)
add_file(os.getenv('tm3'), '3', opts.delete)
add_file(os.getenv('tmg1'), '1', opts.delete)
add_file(os.getenv('tmx1'), '1', opts.delete)

print '----------------[ ppc ]------------------'
for item in ppc_list:
    print '%s %s [%s]' % (item.name, item.ctime, item.client)
print '\n'

print '%50s -------------------[ x86 ]------------------' % ' '
for item in x86_list:
    print '%50s %s %s [%s]' % (' ', item.name, item.ctime, item.client)
print '\n'


