#!/usr/bin/python
import mmap
import os

NVDEV = '/dev/agigcntl'
NVSIZE = 1024 * 1024 * 1024

PATTERN1 = '1'
PATTERN2 = '2'
PATTERN3 = '3'

if not os.path.exists(NVDEV):
    NVDEV = '/dev/umx0'

f = open(NVDEV, 'r+b')
mm = mmap.mmap(f.fileno(), NVSIZE,  flags = mmap.MAP_SHARED, prot = mmap.PROT_READ | mmap.PROT_WRITE)

def write_pattern(pat):
    mm.seek(0)

    for i in xrange((NVSIZE / len(pat)) -  len(pat)):
        mm.write(pat)

def dump(size):
    mm.seek(0)
    f = open('/var/log/nv.bin', 'w')
    f.write(mm.read(size))
    f.close()

dump(NVSIZE)


