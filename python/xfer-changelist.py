#!/usr/bin/python
import os
import optparse
import shutil
import re
import os.path
import time
import sys

class error():
    def __init__ (self, err_string):
        self.err_string = err_string

def run_cmd(command):
    p = os.popen(command)
    s = p.readlines()
    p.close()
    return s

def export_clist(clist):
    numfiles = run_cmd('p4 describe ' + clist + ' | wc -l')

    if numfiles == 0:
        raise error('Changelist ' + clist + ' does not exist')


    numfiles = run_cmd('p4 opened ... | grep ' + clist + ' | wc -l')

    if numfiles == 0:
        raise error('Changelist not in this directory')

    # Create manifest
    p4paths = run_cmd('p4 opened -c ' + clist)
    files = run_cmd('p4 opened -c ' + clist + ' | sed "s:#.*$::" | p4 -x - where | sed "s:.* ::"')

    try:
        os.mkdir('/tmp/' + clist)
    except OSError:
        print('Directory ' + clist + ' already exists. Not creating')

    # Create the file
    fil = open('/tmp/' + clist + '/manifest.txt', 'w')

    for path in p4paths:
        fil.write(path)
    fil.close()

    # Copy files to the xfer directory. Rename to numerical
    i = 0
    for f in files:
        shutil.copy(f.strip(), '/tmp/' + clist + '/' + str(i))
        i = i + 1
    

def import_dir(dir):
    f = open(dir + '/manifest.txt')
    files = f.readlines()
    f.close()

    i = 0
    for fil in files:
        fil = re.sub('\(.*\)', '', fil)
        cmd = 'echo ' + fil.strip() + ' | sed "s:#.*$::"'
        #print cmd
        
        p4file = run_cmd(cmd)
        p4where = run_cmd('p4 where ' + p4file[0])
        m = re.match('(.*) (.*) (.*)', p4where[0])
        dest_file = m.group(3)

        if re.match('.* - add .*', fil):
            shutil.copy(dir + '/' + str(i), dest_file)
            run_cmd('p4 add ' + dest_file)
            print('Adding file ' + dest_file)

        elif re.match('.* - edit .*', fil):
            run_cmd('p4 edit ' + dest_file)
            shutil.copy(dir + '/' + str(i), dest_file)
            print('Editing file ' + dest_file)

        elif re.match('.* - delete .*', fil):
            run_cmd('p4 delete ' + dest_file)
            print('Deleting file ' + dest_file)

        i = i + 1

    
parser = optparse.OptionParser()
parser.add_option('-e', '--export', dest='clist', help='Changelist number to export')
parser.add_option('-i', '--import', dest='dir', help='Directory to import')

(opts, args) = parser.parse_args()

if opts.clist and opts.dir:
    raise error('Only one option can be given. Export or import')

# Export a changelist
if opts.clist:
    export_clist(opts.clist)
elif opts.dir:
    import_dir(opts.dir)
else:
    raise error('Import or Export option needs to be specified')



